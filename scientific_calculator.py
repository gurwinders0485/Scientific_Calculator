import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
import math

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Scientific Calculator")
        self.master.geometry("400x600")
        
        self.current_input = ""
        self.history = []
        self.memory = Decimal(0)

        self.create_widgets()

    def create_widgets(self):
        self.display = tk.Entry(self.master, font=("Arial", 24), justify='right', bd=10, insertwidth=2)
        self.display.grid(row=0, column=0, columnspan=4)

        # Set a default button color
        button_color = '#D3D3D3'  # Light gray color

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),  # Moved '/' to the position of 'log'
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log', 5, 3),  # 'log' remains in its position
            ('exp', 6, 0), ('sqrt', 6, 1), ('M+', 6, 2), ('M-', 6, 3),
            ('H', 7, 1), ('MR', 7, 2), ('MC', 7, 3), ('C', 7, 0)  # Moved 'C' to the last row
        ]

        # Create buttons with the default color
        for (text, row, col) in buttons:
            button = tk.Button(self.master, text=text, font=("Arial", 18), command=lambda t=text: self.on_button_click(t), 
                               width=5, height=2, bg=button_color, relief='raised', borderwidth=5)
            button.grid(row=row, column=col, padx=5, pady=5)

    def on_button_click(self, char):
        if char in '0123456789.':
            self.current_input += char
            self.update_display()
        elif char in '+-*/':
            self.current_input += f' {char} '
            self.update_display()
        elif char == '=':
            self.calculate()
        elif char in ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt']:
            self.calculate_function(char)
        elif char == 'C':
            self.clear()
        elif char == 'H':
            self.show_history()
        elif char == 'M+':
            self.memory += Decimal(self.current_input)
            self.clear()
        elif char == 'M-':
            self.memory -= Decimal(self.current_input)
            self.clear()
        elif char == 'MR':
            self.current_input = str(self.memory)
            self.update_display()
        elif char == 'MC':
            self.memory = Decimal(0)
            self.clear()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.current_input)

    def calculate(self):
        try:
            result = eval(self.current_input.replace('^', '**'))
            self.history.append(f"{self.current_input} = {result}")
            self.current_input = str(result)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", "Invalid input or calculation.")

    def calculate_function(self, func):
        try:
            if func == 'sin':
                result = math.sin(math.radians(Decimal(self.current_input)))
            elif func == 'cos':
                result = math.cos(math.radians(Decimal(self.current_input)))
            elif func == 'tan':
                result = math.tan(math.radians(Decimal(self.current_input)))
            elif func == 'log':
                result = math.log(Decimal(self.current_input))
            elif func == 'exp':
                result = math.exp(Decimal(self.current_input))
            elif func == 'sqrt':
                result = math.sqrt(Decimal(self.current_input))           
            self.history.append(f"{func}({self.current_input}) = {result}")
            self.current_input = str(result)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", "Invalid input for function.")

    def clear(self):
        self.current_input = ""
        self.update_display()

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Calculation History")
        history_window.geometry("300x400")

        history_text = tk.Text(history_window, font=("Arial", 12))
        history_text.pack(expand=True, fill='both')

        for entry in self.history:
            history_text.insert(tk.END, entry + "\n")

        history_text.config(state=tk.DISABLED)  # Make the text read-only

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()