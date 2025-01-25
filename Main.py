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
from kivy.core.audio import SoundLoader

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
            bold=True,  # Make text bold
            size_hint_y=0.2
        )

        # Button grid
        button_grid = GridLayout(cols=4, spacing=10, size_hint_y=0.2)
        buttons = [
            ('Calculator', self.dummy_action),
            ('Add Expense', self.add_expense),
            ('Add Income', self.add_income),
            ('Report', self.view_report)  # Updated to navigate to report
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

    def view_report(self, instance):
        print("Navigating to report screen")
        if self.parent:
            report_screen = self.parent.manager.get_screen('report').children[0]
            report_screen.update_transactions(self.transactions)
            self.parent.manager.current = 'report'

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
                    transaction_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=10, spacing=10)

                    # Left side: Title and Note
                    left_layout = BoxLayout(orientation='horizontal')
                    title_label = Label(
                        text=f"{category}",
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
        self.sound = SoundLoader.load('expense.mp3')  # Load your sound file
        self.build_ui()

    def build_ui(self):
        # Top bar with Back button
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.5)
        top_bar.add_widget(Label(size_hint_x=0.9))
        back_button = Button(
            size_hint=(None, None),
            size=(50, 50),
            background_normal='path/to/your/image.png'
        )
        back_button.bind(on_press=self.go_back)
        top_bar.add_widget(back_button)
        self.add_widget(top_bar)

        # Add Expense title
        self.add_widget(Label(text='Add Expense', font_size='24sp', size_hint_y=0.1))

        # Rest of the expense entry UI
        self.amount_input = TextInput(
            hint_text='Amount',
            input_filter='float',
            multiline=False
        )

        self.category_spinner = Spinner(
            text='Select Category',
            values=('Food', 'Transport', 'Utilities', 'Entertainment', 'Other')
        )

        self.note_input = TextInput(
            hint_text='Note/Description',
            multiline=True
        )

        self.date_input = TextInput(
            text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            multiline=False
        )

        save_button = Button(
            text='Save',
            background_color=(0.4, 0.8, 0.4, 1)
        )
        save_button.bind(on_press=self.save_expense)

        # Add widgets to layout
        self.add_widget(self.amount_input)
        self.add_widget(self.category_spinner)
        self.add_widget(self.note_input)
        self.add_widget(self.date_input)
        self.add_widget(save_button)

    def save_expense(self, instance):
        # Validate inputs
        if not self.amount_input.text or float(self.amount_input.text) <= 0:
            self.show_popup('Error', 'Amount must be a positive number.')
            return
        if self.category_spinner.text == 'Select Category':
            self.show_popup('Error', 'Please select a category.')
            return

        # Play sound
        if self.sound:
            self.sound.play()

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
        self.sound = SoundLoader.load('income.mp3')  # Load your sound file
        self.build_ui()

    def build_ui(self):
        # Top bar with Back button
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.5)
        top_bar.add_widget(Label(size_hint_x=0.9))
        back_button = Button(
            size_hint=(None, None),
            size=(50, 50),
            background_normal='path/to/your/image.png'
        )
        back_button.bind(on_press=self.go_back)
        top_bar.add_widget(back_button)
        self.add_widget(top_bar)

        # Add Income title
        self.add_widget(Label(text='Add Income', font_size='24sp', size_hint_y=0.1))

        # Rest of the income entry UI
        self.amount_input = TextInput(
            hint_text='Amount',
            input_filter='float',
            multiline=False
        )

        self.category_spinner = Spinner(
            text='Select Category',
            values=('Salary', 'Business', 'Investment', 'Gift', 'Other')
        )

        self.note_input = TextInput(
            hint_text='Note/Description',
            multiline=True
        )

        self.date_input = TextInput(
            text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            multiline=False
        )

        save_button = Button(
            text='Save',
            background_color=(0.4, 0.8, 0.4, 1)
        )
        save_button.bind(on_press=self.save_income)

        # Add widgets to layout
        self.add_widget(self.amount_input)
        self.add_widget(self.category_spinner)
        self.add_widget(self.note_input)
        self.add_widget(self.date_input)
        self.add_widget(save_button)

    def save_income(self, instance):
        # Validate inputs
        if not self.amount_input.text or float(self.amount_input.text) <= 0:
            self.show_popup('Error', 'Amount must be a positive number.')
            return
        if self.category_spinner.text == 'Select Category':
            self.show_popup('Error', 'Please select a category.')
            return

        # Play sound
        if self.sound:
            self.sound.play()

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

class ReportScreen(BoxLayout):
    def __init__(self, transactions, **kwargs):
        super(ReportScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10
        self.transactions = transactions
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()  # Clear existing widgets

        # Top bar with Back button
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.025)
        top_bar.add_widget(Label(size_hint_x=0.9))
        back_button = Button(
            size_hint=(None, None),
            size=(50, 50),
            background_normal='background_normal.png'
        )
        back_button.bind(on_press=self.go_back)
        top_bar.add_widget(back_button)
        self.add_widget(top_bar)

        # Report title
        self.add_widget(Label(text='Report Screen', font_size='24sp', size_hint_y=0.05, bold = True))

        # Calculate summary
        income_summary = {}
        expense_summary = {}

        for transaction in self.transactions:
            category = transaction['category']
            amount = float(transaction['amount'])
            if transaction.get('is_income', False):
                if category in income_summary:
                    income_summary[category] += amount
                else:
                    income_summary[category] = amount
            else:
                if category in expense_summary:
                    expense_summary[category] += amount
                else:
                    expense_summary[category] = amount

        # Display income summary
        self.add_widget(Label(text='Income Summary', font_size='20sp', size_hint_y=0.05))
        for category, total in income_summary.items():
            self.add_widget(Label(text=f"{category}: ${total:.2f}", size_hint_y=None, height=30))

        # Display expense summary
        self.add_widget(Label(text='Expense Summary', font_size='20sp', size_hint_y=0.05))
        for category, total in expense_summary.items():
            self.add_widget(Label(text=f"{category}: ${total:.2f}", size_hint_y=None, height=30))

    def update_transactions(self, transactions):
        self.transactions = transactions
        self.build_ui()

    def go_back(self, instance):
        self.parent.manager.current = 'main'

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

        # Report screen
        report_screen = Screen(name='report')
        report_screen.add_widget(ReportScreen(main_screen.children[0].transactions))
        sm.add_widget(report_screen)

        return sm

if __name__ == '__main__':
    AccountApp().run()