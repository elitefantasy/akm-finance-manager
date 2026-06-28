from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty,
    BooleanProperty,
    DictProperty,
)



class DashboardScreen(Screen):
    pass

class AddTransactionScreen(Screen):
    def on_enter(self):
        self.ids.amount.focus = True

class HistoryScreen(Screen):
    pass
    
class ReportScreen(Screen):
    pass
    
class EditTransactionScreen(Screen):
    pass

class StatisticsScreen(Screen):
    pass

class DataManagementScreen(Screen):
    pass


class ManageTransactionsScreen(Screen):
    pass


class ManageRecurringScreen(Screen):
    pass

class CategoryScreen(Screen):
    pass
    
class TransactionRow(BoxLayout):

    category = StringProperty("")
    amount = StringProperty("")
    note = StringProperty("")
    date = StringProperty("")

    amount_color = ListProperty([1,1,1,1])

    transaction_id = NumericProperty(0)

class ClickableTransactionRow(ButtonBehavior, BoxLayout):

    # ---------- Display ----------
    category = StringProperty("")
    amount = StringProperty("")
    note = StringProperty("")
    date = StringProperty("")

    amount_color = ListProperty([1, 1, 1, 1])

    # ---------- Data ----------
    transaction = DictProperty({})

    # ---------- UI ----------
    pressed = BooleanProperty(False)

    # Assigned by FinanceManagerApp
    transaction_callback = None

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

        if callable(self.transaction_callback):
            self.transaction_callback(self.transaction)

class DashboardTransactionRow(ClickableTransactionRow):
    pass

class AddRecentTransactionRow(ClickableTransactionRow):
    pass


class RecurringRow(BoxLayout):

    category = StringProperty("")
    amount = StringProperty("")
    day = StringProperty("")
    last_added = StringProperty("")
    index = NumericProperty(0)
    

class CategoryRow(BoxLayout):

    text = StringProperty("")

    category_id = NumericProperty(0)

class StatisticsRow(BoxLayout):

    category = StringProperty("")

    total = StringProperty("")

    months = StringProperty("")

    average = StringProperty("")

    
    
    
 