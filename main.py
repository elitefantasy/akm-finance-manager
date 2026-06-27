import json
import csv
import os
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from core import backup_service
from core import database_service
from core import reports
from core.transaction_formatter import TransactionFormatter
from core.constants import (
    CSV_EXPORT_FILE,
    DEFAULT_DB,
    SETTINGS_FILE,
    get_backup_dir,
)
from core.database import DatabaseManager
from core.dialogs import DialogManager
from core.logger import get_logger
from core.utils import project_path
from core.icons import Icons
from ui.screens import *
from ui.ui_metrics import (
    Font,
    Size,
    Spacing,
    Padding,
    Radius,
    Color,
)

from kivy.core.text import LabelBase




logger = get_logger(__name__)
BACKUP_DIR = get_backup_dir()

LabelBase.register(
    name="MaterialIcons",
    fn_regular=project_path(
        "assets",
        "fonts",
        "MaterialIcons-Regular.ttf"
    )
)

Builder.load_file(project_path("ui", "finance.kv"))

class FinanceManagerApp(App):
    
    from ui import ui_metrics as metrics
    
    icons = Icons

    balance = NumericProperty(0)
    income = NumericProperty(0)
    expense = NumericProperty(0)
    total_income = NumericProperty(0)
    total_expense = NumericProperty(0)

    
    search_text = StringProperty("")
    recent_text = StringProperty("")
    top_category_text = StringProperty("None")
    monthly_expense_text = StringProperty("₹0")
    
    categories_text = StringProperty("")
    # shows recent transaction in add transaction screen
    add_screen_history = StringProperty("")
    
    current_filter = StringProperty("All")
    current_database=StringProperty(DEFAULT_DB)
    current_screen = StringProperty("dashboard")
    
    selected_transaction_id = None
    
    sort_mode = StringProperty("Newest First")
    
    
    transaction_data = ListProperty([])
    category_data = ListProperty([])
    recurring_data = ListProperty([])
    database_data = ListProperty([])


    def log(self, message):

        os.makedirs(
            BACKUP_DIR,
            exist_ok=True
        )
    
        log_file = os.path.join(
            BACKUP_DIR,
            "debug.log"
        )
    
        with open(
            log_file,
            "a"
        ) as f:
    
            f.write(
                f"{datetime.now()} | {message}\n"
            )
        # use self.log(f"Switch database: {db_name}")

    def build(self):
        self.log(
            "\n========== APP START =========="
        )
        
        # open settings json
        settings_path = os.path.join(
            App.get_running_app().user_data_dir,
            SETTINGS_FILE
        )
        try:
            with open(
                settings_path,"r") as f:
                    settings=json.load(f)
                    
                    db_name=settings.get(
                        "database",
                        DEFAULT_DB)
            self.log(f"loaded database from settings: {db_name}")
                    
                    
        except Exception as e:
            self.log(f"Settings error:{e}")
            
            db_name=DEFAULT_DB
                
        
        self.transactions = []
        self.recurring_transactions = []
        
        self.db = DatabaseManager(db_name)
        self.current_database= self.db.db_name

        self.log(f"Current_database: {self.current_database}")
        self.log(f"Database path: {self.db.db_path}")
        
        self.refresh_database_list()
        
        self.db.create_database()
        
        self.categories = self.db.load_categories_db()
        self.log(f"Categories loaded: {len(self.categories)}")
            
        self.refresh_categories()
        
        self.transactions = self.db.load_transactions_db()
        
        self.recurring_transactions= self.db.load_recurring_db() 

        self.log(f"Transaction loaded: {len(self.transactions)}")
        self.log(f"recurring transactions loaded: {len(self.recurring_transactions)}")

        self.log(f"Build Completed Successfully")

        sm = ScreenManager()
        
        
        
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(AddTransactionScreen(name="add"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(ReportScreen(name="report"))
        sm.add_widget(EditTransactionScreen(name="edit"))
        sm.add_widget(StatisticsScreen(name="statistics"))
        sm.add_widget(DataManagementScreen(name="datamanagement"))
        sm.add_widget(RecurringScreen(name="recurring"))
        sm.add_widget(ManageTransactionsScreen(name="manage_transactions"))
        sm.add_widget(ManageRecurringScreen(name="manage_recurring"))
        sm.add_widget(CategoryScreen(name="categories"))
        
        #self.update_dashboard()
        
        return sm
        
    def on_start(self):

        Clock.schedule_once(
            lambda dt:
            self.update_dashboard(),
            0
        )
        
    def print_db_transactions(self):
        rows = self.db.fetch_query(
            "SELECT * FROM transactions"
        )
        logger.debug("Database transactions: %s", rows)
        
        
         
        self.update_dashboard()
        
    
    
    
    def delete_last(self):

        if not self.transactions:
            return
        
        last_transaction = max(
            self.transactions,
            key=lambda t:t["id"]
            )
        
        self.transaction.remove(
        last_transaction)
        
        self.db.delete_transaction_db(last_transaction["id"])

            
        self.update_dashboard()
    
    def update_sort(self, value):
        self.sort_mode = value
        self.refresh_transaction_view()
    
    def delete_transaction(self,transaction_id):
        
        DialogManager.confirm(
            "Confirm Delete",
            "Delete this transaction?",
            lambda:
            self.confirm_delete(
                transaction_id
            )
        )
    
    def confirm_delete(self,transaction_id):
        self.transactions = [
            t for t in self.transactions
            if t["id"] != transaction_id
        ]

        
        self.db.delete_transaction_db(transaction_id)
        
        self.update_dashboard()
    
    
    def category_report(self):
        return reports.category_report(self.transactions)

    # Transaction Structure
    def add_transaction(self, amount, category, note, ttype):
        try:
            amount = float(amount)
            
            if amount <=0:
                raise ValueError
        
        except:
            DialogManager.show_message(
                "Invalid Input",
                "Please enter a valid amount"
            )
            return
            
        transaction = {
            "type": ttype,
            "amount": (amount),
            "category": category,
            "note": note, 
            "date": datetime.now().strftime("%d-%m-%Y %H:%M")
            }

        transaction["id"] = self.db.save_transaction_db(transaction)
        
        self.transactions.append(transaction)
        
        self.update_dashboard()
        
        add_screen = self.root.get_screen("add")
        add_screen.ids.amount.text=""
        add_screen.ids.note.text=""
        
        
    def refresh_transaction_view(self):

        self.transaction_data = []

        transactions = self.transactions.copy()

        if self.sort_mode == "Newest First":
            transactions.reverse()

        elif self.sort_mode == "Highest Amount":
            transactions.sort(
                key=lambda x: x["amount"],
                reverse=True
            )

        elif self.sort_mode == "Lowest Amount":
            transactions.sort(
                key=lambda x: x["amount"]
            )

        elif self.sort_mode == "Category A-Z":
            transactions.sort(
                key=lambda x: x["category"]
            )

        for t in transactions:

            if (
                self.current_filter != "All"
                and t["type"] != self.current_filter
            ):
                continue

            if self.search_text:

                search = self.search_text.lower()
                
                category = t["category"].lower()
                note = t.get("note", "").lower()
                ttype = t.get("type").lower()
                amount = str(t["amount"])
                
                if (
                    search not in category
                    and search not in note
                    and search not in ttype
                    and search not in amount
                ):
                    continue

            self.transaction_data.append(
                TransactionFormatter.history(t)
            )
            

    def update_dashboard(self):
        income = 0
        expense = 0
    
        for t in self.transactions:
            if t["type"] == "Income":
                income += t["amount"]
            else:
                expense += t["amount"]
    
        self.total_income = income
        self.total_expense = expense
    
        self.income = income
        self.expense = expense
        balance = income - expense

        self.balance = balance
    
        recent = ""
        
        
        
        # recent transaction code
        if not self.root:
          return
        try:
            dashboard = self.root.get_screen("dashboard")
            recent_box = (dashboard.ids.recent_box)
            recent_box.clear_widgets()
            
            for transaction in self.transactions[-5:][::-1]:

                recent_box.add_widget(

                    DashboardTransactionRow(

                        category=transaction["category"],

                        amount=TransactionFormatter.amount(transaction),

                        note=TransactionFormatter.note(transaction),

                        date=TransactionFormatter.date(transaction),

                        amount_color=TransactionFormatter.amount_color(transaction)

                    )

                )
                
              
                            
        except Exception:
            logger.exception("Recent Box Error")
        
        self.refresh_transaction_view()
        self.refresh_add_screen_history()
        self.top_category_text = self.top_category()
        self.monthly_expense_text = self.monthly_expense()

        
    
    from kivy.uix.button import Button

    def refresh_add_screen_history(self):
    
        if not self.root:
            return
        
        try:
            add_screen = self.root.get_screen("add")
            recent_list = add_screen.ids.recent_list
    
            recent_list.clear_widgets()
    
            for t in reversed(self.transactions[-8:]):
    
                row = AddRecentTransactionRow(
                    category=t["category"],
                    amount=TransactionFormatter.amount(t),
                    note=TransactionFormatter.note(t),
                    date=TransactionFormatter.date(t),
                    amount_color=TransactionFormatter.amount_color(t),
                    transaction=t,
                )

                row.use_callback = self.use_recent_transaction

                recent_list.add_widget(row)
    
        except Exception:
            logger.exception("Recent List Error")
    
    
    def update_search(self, text):

        self.search_text = text
        self.refresh_transaction_view()
    
    def update_filter(self, value):

        self.current_filter = value
        self.refresh_transaction_view()
    
    def top_category(self):
        return reports.top_category(self.transactions)

    # also check refresh_add_screen_history(above)
    def recent_transactions(self):

        result = ""

        for t in reversed(
            self.transactions[-5:]
        ):
            sign = "+" if t["type"] == "Income" else "-"
            
            result += (
                f"•{t['category']:<12} "
                f"{sign}₹{t['amount']:.0f}\n"
            )

        return result

    def use_recent_transaction(self, transaction):

        add_screen = self.root.get_screen("add")

        add_screen.ids.category.text = transaction["category"]

        add_screen.ids.note.text = transaction.get("note", "")

        add_screen.ids.amount.text = str(transaction["amount"])

        add_screen.ids.amount.focus = True
    
    def monthly_expense(self):
        return reports.monthly_expense(self.transactions)
    
    def show_message(self, message):

        Popup(
            title="Finance Manager",
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        ).open()
    
    def export_csv(self):

        with open(
            CSV_EXPORT_FILE,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Type",
                "Amount",
                "Category",
                "Date"
            ])

            for t in self.transactions:

                writer.writerow([
                    t["id"],
                    t["type"],
                    t["amount"],
                    t["category"],
                    t["date"]
                ])
                
        DialogManager.show_message(
                "Success",
                "CSV Exported Successfully"
            )
    
    def open_edit(self, transaction_id):

        self.selected_transaction_id = transaction_id

        for t in self.transactions:

            if t["id"] == transaction_id:

                screen = self.root.get_screen("edit")
                
                screen.ids.amount.text = str(t["amount"])
                screen.ids.category.text = t["category"]
                screen.ids.note.text = t.get("note","")
                screen.ids.date.text = t["date"]

                break

        self.root.current = "edit"
    
    def save_edit(self,amount,category, note, date):

        for t in self.transactions:

            if (
                t["id"] == self.selected_transaction_id):
                t["amount"] = float(amount)
                t["category"] = category
                t["note"] = note
                t["date"] = date

                break

        self.db.update_transaction_db(
            self.selected_transaction_id,
            {
                "amount": float(amount),
                "category": category,
                "note": note,
                "date": date
            }
        )
              
        self.update_dashboard()

        self.root.current = "history"
    
    def expense_summary(self):
        return reports.expense_summary(self.transactions)
    


    def category_statistics(self):
        return reports.category_statistics(self.transactions)
    

    def backup_data(self):
    
        try:
            backup_service.backup_database(
                self.db.db_path,
                self.current_database
            )

            self.log(f"Backup created: {self.current_database}")
    
            DialogManager.show_message(
                "Success",
                f"{self.current_database} backed up"
            )
    
        except Exception as e:
    
            DialogManager.show_message(
                "Error",
                str(e)
            )

    # basically import backup
    def import_database(self, filename, popup):

        try:
    
            success, message, db_name = (
                backup_service.import_database_file(
                    filename,
                    App.get_running_app().user_data_dir
                )
            )

            if not success:
                title = "Invalid Database"

                if message in [
                    "Database not found",
                    "Database already exists"
                ]:
                    title = "Error"

                DialogManager.show_message(
                    title,
                    message
                )
                return

            self.refresh_database_list()

            self.log("database imported succesfully")
    
            popup.dismiss()
    
            DialogManager.show_message(
                "Success",
                f"{db_name} imported"
            )
    
        except Exception as e:
    
            DialogManager.show_message(
                "Error",
                str(e)
            )
    
    def show_import_popup(self):

        content = BoxLayout(
            orientation="vertical",
            spacing=Spacing.SMALL,
            padding=Spacing.NORMAL
        )
    
        popup = Popup(
            title="Import Database",
            content=content,
            size_hint=Size.POPUP_MEDIUM
        )
    
        databases = backup_service.list_backup_databases()
    
        if not databases:
    
            content.add_widget(
                Label(
                    text="No backup databases found"
                )
            )
    
        else:
    
            for db in databases:
    
                btn = Button(
                    text=db,
                    size_hint_y=None,
                    height=Size.BUTTON_HEIGHT
                )
    
                btn.bind(
                    on_release=lambda instance,
                    filename=db:
                    self.import_database(
                        filename,
                        popup
                    )
                )
    
                content.add_widget(btn)
    
        popup.open()
            
    def recover_data(self):
        DialogManager.confirm(
            "Confirm Recovery",
            "Recover backup and overwrite current data?",
            self.confirm_recover
        )
            
    def confirm_recover(self):

        try:

            with open("finance_backup.json", "r") as f:
                backup = json.load(f)
                
            if not backup: 
                raise Exception
                
            self.transactions = backup
                
            self.db.execute_query(
            "DELETE FROM transactions")
            
            for transaction in backup:
                self.db.save_transaction_db(transaction)

            
            self.update_dashboard()
            
            
            DialogManager.show_message(
            "Success",
            "Data Recovered"
        )

        except:       
            DialogManager.show_message(
            "Error",
            "No Backup Found"
        )
        
    
    def clear_all_data(self):
        DialogManager.confirm(
            "Warning",
            "Delete all transactions?",
            lambda:
            self.confirm_clear_all_data()
        )
    
    def confirm_clear_all_data(self):
        self.transactions = []
        self.db.clear_transactions_db()

        self.update_dashboard()
        
        DialogManager.show_message(
            "Success",
            "All Data Cleared"
        )
    
    def edit_date_popup(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        day = TextInput(
            hint_text="DD",
            multiline=False
        )

        month = TextInput(
            hint_text="MM",
            multiline=False
        )

        year = TextInput(
            hint_text="YYYY",
            multiline=False
        )

        layout.add_widget(day)
        layout.add_widget(month)
        layout.add_widget(year)

        save_btn = Button(text="Save Date")
        layout.add_widget(save_btn)

        popup = Popup(
            title="Select Date",
            content=layout,
            size_hint=(.8,.6)
        )

        save_btn.bind(
            on_press=lambda x:
            self.save_popup_date(
                day.text,
                month.text,
                year.text,
                popup
            )
        )

        popup.open()
        
    # save popup date
    def save_popup_date(self,day,month,year,popup):

        try:

            date = (
                f"{int(day):02d}-"
                f"{int(month):02d}-"
                f"{year}"
            )

            screen = self.root.get_screen("edit")
            
            old_time = (
                screen.ids.date.text
                .split(" ")[1]
            )

            screen.ids.date.text = (
                f"{date} {old_time}"
            )

            popup.dismiss()
            
        except Exception:
            logger.exception("Date popup error")
            popup.dismiss()
    
    def add_recurring(self, amount, category, day):

        try:

            amount = float(amount)
            day = int(day)

            if amount <= 0:
                raise Exception

            if not 1 <= day <= 31:
                raise Exception

        except:
            DialogManager.show_message(
                "Invalid Input",
                "Enter valid amount and day (1-31)"
            )
            return

        recurring = {
            "amount": amount,
            "category": category,
            "day": day,
            "last_added": ""
        }

        self.recurring_transactions.append(recurring)

        self.db.save_recurring_db(recurring)
       
        self.refresh_recurring_view()
        
        DialogManager.show_message(
            "Sucess",
            "Recurring Expense Added"
        )
        
    
    
    def process_recurring(self):
        today = datetime.now()

        current_period = (f"{today.month}-{today.year}")

        changed = False

        for r in self.recurring_transactions:
            if (today.day == r["day"]
                and r.get(
                    "last_added",""
                ) != current_period):

                transaction = {
                    "type": "Expense",
                    "amount":r["amount"],
                    "category":r["category"],
                    "note":
                    "Recurring",
                    "date":today.strftime("%d-%m-%Y %H:%M")
                }

                transaction["id"] = self.db.save_transaction_db(transaction)

                self.transactions.append(transaction)

                r["last_added"] = (current_period)

                changed = True

        if changed:

            self.db.update_recurring_db(
                r["id"],
                {"last_added":current_period})

            self.update_dashboard()
    
    def refresh_recurring_view(self):

        data = []

        for i, r in enumerate(
            self.recurring_transactions
        ):

            data.append({

                "text":
                f"₹{r['amount']}\n"
                f"{r['category']}\n"
                f"Day {r['day']}",

                "index": i
            })

        self.recurring_data = data
    
    def save_recurring_edit(self,index,amount,category,day,popup):
        try:
            amount = float(amount)
            day = int(day)
            if not 1 <= day <= 31:
                raise Exception
        except:
            return

        recurring = (
            self.recurring_transactions[index]
        )

        recurring["amount"] = amount
        recurring["category"] = category
        recurring["day"] = day
        
        self.db.update_recurring_db(
            recurring["id"],
        {
            "amount": amount,
            "category": category,
            "day": day
        }
        )

        self.refresh_recurring_view()

        popup.dismiss()

        
    
    def delete_recurring(self, index):

        if (
            index < 0
            or index >= len(
                self.recurring_transactions
            )
        ):
            return

        recurring = (
            self.recurring_transactions.pop(index))
        
        self.db.delete_recurring_db(recurring["id"])

        self.refresh_recurring_view()
    
    
    def edit_recurring(self, index):

        recurring = (self.recurring_transactions[index])

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        amount = TextInput(
            text=str(recurring["amount"]),
            multiline=False
        )

        category = Spinner(
            text=recurring["category"],
            values=self.categories
        )

        day = TextInput(
            text=str(recurring["day"]),
            multiline=False
        )

        save_btn = Button(
            text="Save"
        )

        layout.add_widget(amount)
        layout.add_widget(category)
        layout.add_widget(day)
        layout.add_widget(save_btn)

        popup = Popup(
            title="Edit Recurring",
            content=layout,
            size_hint=(.8,.7)
        )

        save_btn.bind(
            on_press=lambda x:
            self.save_recurring_edit(
                index,
                amount.text,
                category.text,
                day.text,
                popup
            )
        )

        popup.open()

    def open_manage_recurring(self):

        self.refresh_recurring_view()

        self.root.current = (
            "manage_recurring"
        )
   
    def add_category(self, name):
        name = name.strip()

        if not name:
            DialogManager.show_message(
                "Error",
                "Enter category name"
            )
            return
           

        if name in self.categories:
            DialogManager.show_message(
                "error",
                "category already exists"
            )
            return
           

        self.db.save_category_db(name)
        
        self.categories = self.db.load_categories_db()
        
        self.refresh_categories()
        
        DialogManager.show_message(
                "Success",
                "Category Added"
            )
           
    
    def refresh_categories(self):
        rows = self.db.fetch_query(
            """
            SELECT *
            FROM categories
            ORDER BY name
            """
        )

        self.category_data = []

        self.categories = []

        for row in rows:
            self.categories.append(
                row["name"]
            )

            self.category_data.append({
                "text": row["name"],
                "category_id":
                row["id"]
            })
        
        try:
            spinner = self.root.get_screen(
                "add"
            ).ids.category
            spinner.values = self.categories
            
            if spinner.text not in self.categories:
                spinner.text = self.categories[0]
        
        except:
            pass
        
        try:
            spinner = self.root.get_screen(
                "recurring"
            ).ids.category
            spinner.values = self.categories
            
            if spinner.text not in self.categories:
                spinner.text = self.categories[0]
                
        except:
            pass
    
    def delete_category(self,category_id):

        self.db.delete_category_db(category_id)

        self.categories = self.db.load_categories_db()
        
        self.refresh_categories()
    
    def edit_category(self,category_id,old_name):
        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        name = TextInput(
            text=old_name,
            multiline=False
        )

        save = Button(
            text="Save"
        )

        layout.add_widget(name)

        layout.add_widget(save)

        popup = Popup(
            title="Edit Category",
            content=layout,
            size_hint=(.8,.4)
        )

        save.bind(
            on_press=lambda x:
            self.save_category_edit(
                category_id,
                name.text,
                popup
            )
        )

        popup.open()
    
    def save_category_edit(self,category_id,name,popup):

        self.db.update_category_db(
            category_id,
            name.strip()
        )

        self.categories = (
            self.db.load_categories_db()
        )

        self.refresh_categories()

        popup.dismiss()

    def use_recent_category(self, category):
        add_screen = self.root.get_screen("add")
        add_screen.ids.category.text = category
        add_screen.ids.amount.focus = True
    
    def create_database_popup(self):
        layout=BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10)
            
        name=TextInput(
            hint_text="Database Name",
            multiline=False)
        
        create_btn=Button(text="Create")
        
        layout.add_widget(name)
        layout.add_widget(create_btn)
        
        popup=Popup(
            title="Create Database",
            content=layout,
            size_hint=(.8,.4))
        
        create_btn.bind(
            on_press=lambda x:
                self.create_new_database(name.text,popup))

        self.log(f"opening create database popup")
        
        popup.open()
    
    def create_new_database(self,name,popup):
        try:
            db_name = database_service.create_database(name)
        except Exception as e:
            DialogManager.show_message("Error", str(e))
            return
        
        popup.dismiss()

        self.log(f"database created: {db_name}")
        
        DialogManager.show_message(
            "Success",
            f"Created{db_name}")
        
        self.refresh_database_list()
        
        
        
        
    def switch_database(self,db_name):
        if hasattr(self,"db"):
            self.db.conn.close()

        self.log(f"saving databae: {db_name}")

        database_service.save_selected_database(
            App.get_running_app().user_data_dir,
            db_name
        )
                    
        self.db=DatabaseManager(db_name)
        
        self.current_database=(db_name)
        
        self.categories=self.db.load_categories_db()
        self.transactions=(self.db.load_transactions_db())
        self.recurring_transactions =(self.db.load_recurring_db())
        
        self.refresh_categories()
        self.refresh_recurring_view()
        self.update_dashboard()
        
    
    def refresh_database_list(self):
        self.database_data = [
            {
                "db_name": db
            }
            for db in database_service.list_databases(
                App.get_running_app().user_data_dir
            )
        ]
            
    def rename_database_popup(self,old_name):
      layout=BoxLayout(
        orientation="vertical",
        spacing=10,
        padding=10)
        
      name_input=TextInput(
        text=old_name.replace(".db",""),
        multiline=False)
      
      save_btn=Button(text="Save")
      
      layout.add_widget(name_input)
      layout.add_widget(save_btn)
      
      popup=Popup(
        title="Rename Database",
        content=layout,
        size_hint=(.8,.4))
      
      save_btn.bind(
        on_press=lambda x:
          self.rename_database(
            old_name,
            name_input.text,
            popup))
      
      popup.open()
    
    def rename_database(self,old_name,new_name,popup):
        user_dir = App.get_running_app().user_data_dir
        is_current_database = self.current_database == old_name

        try:
            if is_current_database:
                self.db.conn.close()

            success, message, db_name = (
                database_service.rename_database_file(
                    user_dir,
                    old_name,
                    new_name,
                    self.current_database
                )
            )

            if not success:
                if is_current_database:
                    self.db = DatabaseManager(old_name)

                DialogManager.show_message(
                    "Error",
                    message
                )
                return

            if is_current_database:
                self.current_database = db_name
                self.db = DatabaseManager(db_name)

        except Exception as e:
            if is_current_database:
                self.db = DatabaseManager(old_name)

            DialogManager.show_message(
                "Error",
                str(e)
            )
            return

        self.log(f"database renamed: {old_name} -> {db_name}")
        self.refresh_database_list()
        popup.dismiss()
    
    def delete_database_popup(self,db_name):

        self.log(f"opening delete database popup")
        
        if db_name == self.current_database:
            DialogManager.show_message(
                "Error",
                "Cannot delete current database"
            )
            return

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        layout.add_widget(
            Label(
                text=f"Delete {db_name}?"))

        buttons = BoxLayout(
            spacing=10
        )
        yes_btn = Button(
            text="Yes"
        )
        no_btn = Button(
            text="No"
        )

        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)

        layout.add_widget(buttons)

        popup = Popup(
            title="Confirm Delete",
            content=layout,
            size_hint=(.8,.4)
        )

        yes_btn.bind(
            on_press=lambda x:
            self.delete_database(
                db_name,
                popup
            )
        )

        no_btn.bind(
            on_press=lambda x:
            popup.dismiss()
        )

        popup.open()
    
    def delete_database(self,db_name,popup):
        try:
            success, message = (
                database_service.delete_database_file(
                    App.get_running_app().user_data_dir,
                    db_name,
                    self.current_database
                )
            )

            if not success:
                DialogManager.show_message(
                    "Error",
                    message
                )
                return

            self.refresh_database_list()
            popup.dismiss()
            DialogManager.show_message(
                "Success",
                f"{db_name} deleted"
            )
            self.log(f"database deleted succesfully")

        except Exception as e:
          DialogManager.show_message(
               "Error",
              str(e)
          )

    def more_menu(self):

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        categories = Button(text="Categories")

        data = Button(text="Data Management")
        
        statistics=Button(
          text="statistics")

        layout.add_widget(categories)

        layout.add_widget(data)
        
        layout.add_widget(statistics)

        popup = Popup(title="More",
            content=layout,
            size_hint=(.8,.5)
        )

        categories.bind(
            on_press=lambda x:
            self.open_screen(
                "categories",
                popup
            )
        )

        data.bind(
            on_press=lambda x:
            self.open_screen(
                "datamanagement",
                popup
            )
        )
        
        statistics.bind(
          on_press=lambda x:
            self.open_screen(
              "statistics",popup))

        popup.open()

    def open_screen(self,screen_name,popup):
        self.go_to_screen(screen_name)
        popup.dismiss()
    
    def go_to_screen(self, screen_name):
        self.root.current = screen_name
        self.current_screen = screen_name

    

FinanceManagerApp().run()
