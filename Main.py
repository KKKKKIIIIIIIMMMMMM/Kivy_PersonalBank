import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from datetime import datetime

TRANSACTIONS_FILE = 'transactions.json'

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        self.transactions = []  # List to store transactions
        self.balance = 0.0  # Initialize balance
        self.build_ui()
        self.load_transactions()

    def build_ui(self):
        # Account header
        header = BoxLayout(size_hint_y=0.1)
        account_label = Label(
            text='TEST1',
            color=(0.7, 0.7, 1, 1),
            font_size='24sp',
            halign='left'
        )
        header.add_widget(account_label)

        self.balance_label = Label(
            text=f'${self.balance:.2f}',
            font_size='48sp',
            size_hint_y=0.2
        )

        # Button grid
        button_grid = GridLayout(cols=4, spacing=10, size_hint_y=0.2)
        buttons = [
            ('Calculator', self.dummy_action),
            ('Add Expense', self.add_expense),
            ('Add Income', self.add_income),
            ('Report', self.dummy_action)
        ]
        for text, action in buttons:
            btn = Button(
                text=text,
                background_color=(0.4, 0.4, 0.6, 1),
                color=(0.7, 0.7, 1, 1)
            )
            btn.bind(on_press=action)
            button_grid.add_widget(btn)

        # Recent History section
        history_label = Label(
            text='Recent History',
            color=(0.7, 0.7, 1, 1),
            size_hint_y=0.1,
            font_size='24sp'
        )

        # Scrollable transaction list
        scroll_view = ScrollView(size_hint=(1, 0.5))
        self.transactions_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.transactions_layout.bind(minimum_height=self.transactions_layout.setter('height'))
        scroll_view.add_widget(self.transactions_layout)

        # Add all widgets to main layout
        self.add_widget(header)
        self.add_widget(self.balance_label)
        self.add_widget(button_grid)
        self.add_widget(history_label)
        self.add_widget(scroll_view)

    def dummy_action(self, instance):
        print("Dummy action triggered")

    def add_expense(self, instance):
        print("Navigating to expense entry screen")
        if self.parent:
            self.parent.manager.current = 'expense_entry'

    def add_income(self, instance):
        print("Navigating to income entry screen")
        if self.parent:
            self.parent.manager.current = 'income_entry'

    def add_transaction(self, amount, category, note, date, is_income=False):
        amount = float(amount)
        transaction = {
            "amount": amount,
            "category": category,
            "note": note,
            "date": date,
            "is_income": is_income
        }
        self.transactions.append(transaction)
        self.save_transactions()

        # Update balance
        if is_income:
            self.balance += amount
        else:
            self.balance -= amount
        self.update_balance_label()

        # Create layout for transaction
        transaction_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=10, spacing=10)

        # Left side: Title and Note
        left_layout = BoxLayout(orientation='vertical')
        title_label = Label(
            text=f"Title: {category}",
            color=(0.7, 0.6, 1, 1),
            bold=True
        )
        note_label = Label(
            text=f"Note: {note}\n{date}",
            color=(0.7, 0.6, 1, 1)
        )
        left_layout.add_widget(title_label)
        left_layout.add_widget(note_label)

        # Right side: Amount
        amount_label = Label(
            text=f"${amount:.2f}",
            color=(0.5, 1, 0.5, 1) if is_income else (1, 0.5, 0.5, 1),
            bold=True
        )

        # Add to transaction layout
        transaction_layout.add_widget(left_layout)
        transaction_layout.add_widget(amount_label)

        # Add to transactions layout
        self.transactions_layout.add_widget(transaction_layout)

    def update_balance_label(self):
        self.balance_label.text = f'${self.balance:.2f}'

    def save_transactions(self):
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump(self.transactions, f, indent=4)

    def load_transactions(self):
        try:
            with open(TRANSACTIONS_FILE, 'r') as f:
                self.transactions = json.load(f)
                for transaction in self.transactions:
                    amount = float(transaction['amount'])
                    is_income = transaction.get('is_income', False)
                    category = transaction['category']
                    note = transaction['note']
                    date = transaction['date']

                    # Create layout for transaction
                    transaction_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=10, spacing=10)

                    # Left side: Title and Note
                    left_layout = BoxLayout(orientation='vertical')
                    title_label = Label(
                        text=f"Title: {category}",
                        color=(0.7, 0.6, 1, 1),
                        bold=True
                    )
                    note_label = Label(
                        text=f"Note: {note}\non {date}",
                        color=(0.7, 0.6, 1, 1)
                    )
                    left_layout.add_widget(title_label)
                    left_layout.add_widget(note_label)

                    # Right side: Amount
                    amount_label = Label(
                        text=f"${amount:.2f}",
                        color=(0.5, 1, 0.5, 1) if is_income else (1, 0.5, 0.5, 1),
                        bold=True
                    )

                    # Add to transaction layout
                    transaction_layout.add_widget(left_layout)
                    transaction_layout.add_widget(amount_label)

                    # Add to transactions layout
                    self.transactions_layout.add_widget(transaction_layout)

                    # Update balance
                    if is_income:
                        self.balance += amount
                    else:
                        self.balance -= amount
                self.update_balance_label()
        except FileNotFoundError:
            print("No previous transactions found.")
        except ValueError as e:
            print(f"Error loading transactions: {e}")

class ExpenseEntryScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(ExpenseEntryScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        self.build_ui()

    def build_ui(self):
        # Amount input
        self.amount_input = TextInput(
            hint_text='Amount',
            input_filter='float',
            multiline=False
        )

        # Category selector
        self.category_spinner = Spinner(
            text='Select Category',
            values=('Food', 'Transport', 'Utilities', 'Entertainment', 'Other')
        )

        # Note input
        self.note_input = TextInput(
            hint_text='Note/Description',
            multiline=True
        )

        # Date/Time input
        self.date_input = TextInput(
            text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            multiline=False
        )

        # Save button
        save_button = Button(
            text='Save',
            background_color=(0.4, 0.8, 0.4, 1)
        )
        save_button.bind(on_press=self.save_expense)

        # Back button
        back_button = Button(
            text='Back',
            background_color=(0.8, 0.4, 0.4, 1)
        )
        back_button.bind(on_press=self.go_back)

        # Add widgets to layout
        self.add_widget(Label(text='Add Expense', font_size='24sp', size_hint_y=0.1))
        self.add_widget(self.amount_input)
        self.add_widget(self.category_spinner)
        self.add_widget(self.note_input)
        self.add_widget(self.date_input)
        self.add_widget(save_button)
        self.add_widget(back_button)

    def save_expense(self, instance):
        # Validate inputs
        if not self.amount_input.text or float(self.amount_input.text) <= 0:
            self.show_popup('Error', 'Amount must be a positive number.')
            return
        if self.category_spinner.text == 'Select Category':
            self.show_popup('Error', 'Please select a category.')
            return

        # Add transaction to main screen
        main_screen = self.parent.manager.get_screen('main').children[0]
        main_screen.add_transaction(
            self.amount_input.text,
            self.category_spinner.text,
            self.note_input.text,
            self.date_input.text
        )

        # Clear fields
        self.amount_input.text = ''
        self.category_spinner.text = 'Select Category'
        self.note_input.text = ''
        self.date_input.text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Show confirmation
        self.show_popup('Success', 'Expense saved successfully.')

        # Return to main screen
        self.parent.manager.current = 'main'

    def go_back(self, instance):
        self.parent.manager.current = 'main'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class IncomeEntryScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(IncomeEntryScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        self.build_ui()

    def build_ui(self):
        # Amount input
        self.amount_input = TextInput(
            hint_text='Amount',
            input_filter='float',
            multiline=False
        )

        # Category selector
        self.category_spinner = Spinner(
            text='Select Category',
            values=('Salary', 'Business', 'Investment', 'Gift', 'Other')
        )

        # Note input
        self.note_input = TextInput(
            hint_text='Note/Description',
            multiline=True
        )

        # Date/Time input
        self.date_input = TextInput(
            text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            multiline=False
        )

        # Save button
        save_button = Button(
            text='Save',
            background_color=(0.4, 0.8, 0.4, 1)
        )
        save_button.bind(on_press=self.save_income)

        # Back button
        back_button = Button(
            text='Back',
            background_color=(0.8, 0.4, 0.4, 1)
        )
        back_button.bind(on_press=self.go_back)

        # Add widgets to layout
        self.add_widget(Label(text='Add Income', font_size='24sp', size_hint_y=0.1))
        self.add_widget(self.amount_input)
        self.add_widget(self.category_spinner)
        self.add_widget(self.note_input)
        self.add_widget(self.date_input)
        self.add_widget(save_button)
        self.add_widget(back_button)

    def save_income(self, instance):
        # Validate inputs
        if not self.amount_input.text or float(self.amount_input.text) <= 0:
            self.show_popup('Error', 'Amount must be a positive number.')
            return
        if self.category_spinner.text == 'Select Category':
            self.show_popup('Error', 'Please select a category.')
            return

        # Add transaction to main screen
        main_screen = self.parent.manager.get_screen('main').children[0]
        main_screen.add_transaction(
            self.amount_input.text,
            self.category_spinner.text,
            self.note_input.text,
            self.date_input.text,
            is_income=True
        )

        # Clear fields
        self.amount_input.text = ''
        self.category_spinner.text = 'Select Category'
        self.note_input.text = ''
        self.date_input.text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Show confirmation
        self.show_popup('Success', 'Income saved successfully.')

        # Return to main screen
        self.parent.manager.current = 'main'

    def go_back(self, instance):
        self.parent.manager.current = 'main'

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class AccountApp(App):
    def build(self):
        # Set window color
        Window.clearcolor = (0.2, 0.2, 0.2, 1)

        # Screen manager
        sm = ScreenManager()

        # Main screen
        main_screen = Screen(name='main')
        main_screen.add_widget(MainScreen())
        sm.add_widget(main_screen)

        # Expense entry screen
        expense_entry_screen = Screen(name='expense_entry')
        expense_entry_screen.add_widget(ExpenseEntryScreen())
        sm.add_widget(expense_entry_screen)

        # Income entry screen
        income_entry_screen = Screen(name='income_entry')
        income_entry_screen.add_widget(IncomeEntryScreen())
        sm.add_widget(income_entry_screen)

        return sm

if __name__ == '__main__':
    AccountApp().run()