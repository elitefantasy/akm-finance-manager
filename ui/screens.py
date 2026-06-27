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

class RecurringScreen(Screen):
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

class DashboardTransactionRow(ButtonBehavior, BoxLayout):

    category = StringProperty("")
    amount = StringProperty("")
    note = StringProperty("")
    date = StringProperty("")

    amount_color = ListProperty([1, 1, 1, 1])

    transaction = DictProperty({})

    pressed = BooleanProperty(False)

    on_transaction = None

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

        if callable(self.on_transaction):
            self.on_transaction(self.transaction)

class AddRecentTransactionRow(ButtonBehavior, BoxLayout):

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

    # Callback supplied by FinanceManagerApp
    use_callback = None

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

        if callable(self.use_callback):
            self.use_callback(self.transaction)


class RecurringRow(BoxLayout):

    text = StringProperty("")
    index = NumericProperty(0)
    

class CategoryRow(BoxLayout):

    text = StringProperty("")

    category_id = NumericProperty(0)

    
    
    
 