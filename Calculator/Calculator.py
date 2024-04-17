import tkinter as tk
import tkinter.font as font
from decimal import Decimal
from PIL import Image, ImageTk  # Import Image and ImageTk modules from PIL

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.equation = ""
        self.history = []  # Changed to store tuples (expression, result)

        # Set the default window size
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry(f"{screen_width//4}x{screen_height//2}")

        # Load the custom logo image
        logo_image = Image.open("C:\\Users\\Ankit Singh\\Downloads\\logoCal.png")  # Replace "your_logo.png" with the filename of your logo image
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Set the custom logo as the application icon
        self.master.iconphoto(False, logo_photo)

        self.entry = tk.Text(master, font=('arial', 20, 'bold'), bd=30, insertwidth=4, width=14, height=2)
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'H', 'D'  # Added 'D' for the delete history entry button
        ]

        row_val = 1
        col_val = 0

        self.button_widgets = []

        # Set custom font size for button labels
        button_font = font.Font(size=16)

        for button in buttons:
            command = lambda x=button: self.click(x)
            btn = tk.Button(master, text=button, font=button_font, command=command)
            btn.grid(row=row_val, column=col_val, sticky="nsew")
            self.button_widgets.append(btn)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Add a clear button
        self.clear_button = tk.Button(master, text='Clear', font=button_font, command=self.clear)
        self.clear_button.grid(row=row_val, column=0, sticky="nsew")
        self.button_widgets.append(self.clear_button)

        # Add a history button
        self.history_button = tk.Button(master, text='History', font=button_font, command=lambda: self.click('H'))
        self.history_button.grid(row=row_val, column=1, sticky="nsew")
        self.button_widgets.append(self.history_button)

        # Add a delete history entry button
        self.delete_history_button = tk.Button(master, text='Delete', font=button_font, command=lambda: self.click('D'))
        self.delete_history_button.grid(row=row_val, column=2, sticky="nsew")
        self.button_widgets.append(self.delete_history_button)

        # Add a switch theme button
        self.theme_button = tk.Button(master, text="Switch Theme", font=button_font, command=self.switch_theme)
        self.theme_button.grid(row=row_val, column=3, sticky="nsew")
        self.button_widgets.append(self.theme_button)

        # Make the app responsive
        for i in range(6):  # there are 6 rows in the grid
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(4):  # there are 4 columns in the grid
            self.master.grid_columnconfigure(i, weight=1)

        # Set the initial theme
        self.dark_theme = False
        self.switch_theme()

        # Bind keyboard input
        self.master.bind('<Key>', self.key_press)

    def click(self, button):
        if button == '=':
            try:
                # Use the decimal module for more precise division
                result = str(eval(self.equation, {'__builtins__': None}, {'Decimal': Decimal}))
                self.history.append((self.equation, result))  # Store both expression and result in history
                self.equation = result  # Set the equation to the result for further calculations
            except ZeroDivisionError:
                self.equation = "Cannot divide by zero"
            except SyntaxError:
                self.equation = "Invalid input"
        elif button == 'C':
            self.equation = ''
        elif button == 'H':  # If the 'H' button is pressed, show the history
            self.equation = '\n'.join([f"{expr} = {result}" for expr, result in self.history])
            self.update_entry()
        elif button == 'D' and self.equation.strip() == '\n'.join([f"{expr} = {result}" for expr, result in self.history]):
            # Delete most recent history entry
            if self.history:
                self.history.pop()
                self.equation = '\n'.join([f"{expr} = {result}" for expr, result in self.history])
                self.update_entry()
            else:
                self.equation = "History is empty"
                self.update_entry()
        elif button == 'D':
            if self.equation:
                self.equation = self.equation[:-1]  # Delete the most recent input character
                self.update_entry()
        else:
            self.equation += button
        self.update_entry()

    def clear(self):
        self.equation = ''
        self.update_entry()

    def update_entry(self):
        self.entry.delete('1.0', tk.END)
        self.entry.insert(tk.END, self.equation)

    def switch_theme(self):
        # Switch the theme
        self.dark_theme = not self.dark_theme

        if self.dark_theme:
            bg_color = "#070812"  # dark blue
            fg_color = "#ffffff"  # white blue
        else:
            bg_color = "#ffffff"  # white
            fg_color = "#000000"  # black

        # Apply the theme
        self.master.config(bg=bg_color)
        self.entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        for button in self.button_widgets:
            button.config(bg=bg_color, fg=fg_color)

    def key_press(self, event):
        valid_characters = '0123456789.+-/*'
        if event.char in valid_characters:
            self.equation += event.char
            self.update_entry()
        elif event.keysym == 'Return':
            self.click('=')
        elif event.keysym == 'BackSpace':
            self.equation = self.equation[:-1]
            self.update_entry()

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Calculator(root)
    root.mainloop()
