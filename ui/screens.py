from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ListProperty
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

class DashboardTransactionRow(BoxLayout):

    category = StringProperty("")
    amount = StringProperty("")
    note = StringProperty("")
    date = StringProperty("")

    amount_color = ListProperty([1,1,1,1])

class RecurringRow(BoxLayout):

    text = StringProperty("")
    index = NumericProperty(0)
    

class CategoryRow(BoxLayout):

    text = StringProperty("")

    category_id = NumericProperty(0)

    
    
    
 