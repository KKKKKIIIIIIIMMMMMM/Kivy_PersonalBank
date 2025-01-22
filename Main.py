from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

class AccountApp(App):
    def build(self):
        # Set window color
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Account header
        header = BoxLayout(size_hint_y=0.1)
        account_label = Label(
            text='TEST1',
            color=(0.7, 0.7, 1, 1),
            font_size='24sp',
            halign='left'
        )
        header.add_widget(account_label)
        

        balance_label = Label(
            text='$0.00',
            font_size='48sp',
            size_hint_y=0.2
        )
        
        # Button grid
        button_grid = GridLayout(cols=4, spacing=10, size_hint_y=0.2)
        buttons = [
            'Calculator', 'Add Expense', 'Add Income', 'Report'
        ]
        for text in buttons:
            btn = Button(
                text=text,
                background_color=(0.4, 0.4, 0.6, 1),
                color=(0.7, 0.7, 1, 1)
            )
            button_grid.add_widget(btn)
            
        # Recent History section
        history_label = Label(
            text='Recent History',
            color=(0.7, 0.7, 1, 1),
            size_hint_y=0.1,
            font_size='24sp'
        )
        
        # Transaction list (empty)
        transactions_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        transactions_layout.bind(minimum_height=transactions_layout.setter('height'))
        

        # Example transaction
        example_transaction = Label(
            text='- $50.00 Grocery Shopping',
            color=(1, 0.5, 0.5, 1),
            size_hint_y=None,
            height=40
        )
        transactions_layout.add_widget(example_transaction)

        
        # Add all widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(balance_label)
        main_layout.add_widget(button_grid)
        main_layout.add_widget(history_label)
        main_layout.add_widget(transactions_layout)
        
        return main_layout

if __name__ == '__main__':
    AccountApp().run()