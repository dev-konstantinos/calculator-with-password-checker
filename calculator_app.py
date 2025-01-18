import tkinter as tk
from tkinter import font, messagebox

# Hauptlogik und GUI des Taschenrechners
class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Taschenrechner")
        self.setup_geometry()
        self.create_fonts()
        self.create_widgets()
        self.current_input = ""
        self.result = None
        self.operator = None
        self.root.mainloop()

    def setup_geometry(self):
        window_width = 300
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        pos_top = (screen_height // 2) - (window_height // 2)
        pos_left = (screen_width // 2) - (window_width // 2)
        self.root.geometry(f"{window_width}x{window_height}+{pos_left}+{pos_top}")
        self.root.resizable(False, False)

    def create_fonts(self):
        self.display_font = font.Font(family="Arial", size=24, weight="bold")
        self.button_font = font.Font(family="Arial", size=24)

    def create_widgets(self):
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=self.display_font,
            justify="right",
            state="readonly",
            bd=10,
            relief="ridge"
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("C", 4, 0), ("0", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(
                self.root,
                text=text,
                font=self.button_font,
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(row=row, column=col, sticky="nsew")

        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.root.grid_columnconfigure(j, weight=1)

        self.root.bind("<Key>", self.key_press)

    def key_press(self, event):
        key = event.char

        if key.isdigit() or key == ".":
            self.append_to_input(key)
        elif key in "+-*/":
            self.set_operator(key)
        elif key == "\r":
            self.calculate_result()
        elif key == "\x08":
            self.clear()

    def on_button_click(self, button_text):
        if button_text.isdigit() or button_text == ".":
            self.append_to_input(button_text)
        elif button_text in "+-*/":
            self.set_operator(button_text)
        elif button_text == "=":
            self.calculate_result()
        elif button_text == "C":
            self.clear()

    def append_to_input(self, value):
        if self.current_input == "0" and value != ".":
            self.current_input = value
        else:
            self.current_input += value
        self.display_var.set(self.current_input)

    def set_operator(self, operator):
        if self.current_input:
            self.result = float(self.current_input) if self.result is None else self.result
            self.current_input = ""
        self.operator = operator
        self.display_var.set(self.result)

    def calculate_result(self):
        if not self.current_input or not self.operator:
            return
        try:
            second_operand = float(self.current_input)
            if self.operator == "+":
                self.result += second_operand
            elif self.operator == "-":
                self.result -= second_operand
            elif self.operator == "*":
                self.result *= second_operand
            elif self.operator == "/":
                if second_operand == 0:
                    raise ZeroDivisionError
                self.result /= second_operand

            if self.result.is_integer():
                self.result = int(self.result)
            
            self.display_var.set(str(self.result))
            self.current_input = ""
            self.operator = None
        except ZeroDivisionError:
            messagebox.showerror("Fehler", "Division durch Null ist nicht erlaubt!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")
            self.clear()

    def clear(self):
        self.current_input = ""
        self.result = None
        self.operator = None
        self.display_var.set("0")

# Passwort Eingabe und Taschenrechner starten
class PasswordApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PASS")
        self.setup_geometry()
        self.create_fonts()
        self.correct_password = "12345"
        self.create_widgets()
        self.root.mainloop()

    def setup_geometry(self):
        window_width = 240
        window_height = 140
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        pos_top = (screen_height // 2) - (window_height // 2)
        pos_left = (screen_width // 2) - (window_width // 2)
        self.root.geometry(f"{window_width}x{window_height}+{pos_left}+{pos_top}")
        self.root.resizable(False, False)

    def create_fonts(self):
        self.small_font = font.Font(family="Arial", size=12)

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Geben Sie Ihr Passwort ein:", font=("Arial", 12, "bold"))
        self.label.pack(pady=10)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.root, textvariable=self.password_var, show="*", font=self.small_font)
        self.password_entry.pack(pady=5)

        self.password_entry.bind("<Return>", lambda event: self.check_password())
        self.submit_button = tk.Button(self.root, text="Einreichen", font=self.small_font, command=self.check_password)
        self.submit_button.pack(side="left", padx=20)
        self.quit_button = tk.Button(self.root, text="Beenden", font=self.small_font, command=self.root.quit)
        self.quit_button.pack(side="right", padx=20)

    def check_password(self):
        entered_password = self.password_var.get()
        if entered_password == self.correct_password:
            self.root.destroy()
            Calculator()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort. Bitte versuchen Sie es erneut.")
            self.password_var.set("")

if __name__ == "__main__":
    PasswordApp()