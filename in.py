import tkinter as tk
from tkinter import messagebox
from functions import connection_BD
# =======Окно программы для входа=======
class In(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Вход в систему")
        self.geometry("600x600")
        self.config(bg="#cdc5c2")
        self.resizable(False, False)
        self.center()
        self.content()
# Функция - Центрирование окна
    def center(self):
        width_ok = 600
        height_ok = 600
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = int((width_screen / 2) - (width_ok / 2))
        y = int((height_screen / 2) - (height_ok / 2))
        self.geometry(f"{width_ok}x{height_ok}+{x}+{y}")
# Функция - Создание клавиатуры (содержимое окна)
    def content(self):
        tk.Label(self, text="Добро пожаловать!", font=("Bookman Old Style", 33), bg="#cdc5c2").pack(pady=(10, 20))
        tk.Label(self, text="Введите код", font=("Bookman Old Style", 15), bg="#cdc5c2").pack(pady=(30, 10))
        self.password_entry = tk.Entry(self, show='*', font=("Bookman Old Style", 14))
        self.password_entry.pack(pady=30)
 # Кнопки клавиатуры
        self.keyboard_button = tk.Frame(self, bg="#cdc5c2")
        self.keyboard_button.pack(pady=10)
        for i in range(1, 10):
            button_num = tk.Button(self.keyboard_button, text=str(i), command=lambda i=i: self.add_symbol(str(i)), width=5, height=2, font=("Bookman Old Style", 14))
            button_num.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)
        bottom_row_frame = tk.Frame(self, bg="#cdc5c2")
        bottom_row_frame.pack(pady=10)
        delete_button = tk.Button(bottom_row_frame, text="×", command=self.clear, width=5, height=2, font=("Bookman Old Style", 14))
        delete_button.grid(row=0, column=0, padx=5)
        zero_button = tk.Button(bottom_row_frame, text="0", command=lambda: self.add_symbol('0'), width=5, height=2, font=("Bookman Old Style", 14))
        zero_button.grid(row=0, column=1, padx=5)
        next_button = tk.Button(bottom_row_frame, text="→", command=self.check_password, width=5, height=2, font=("Bookman Old Style", 14))
        next_button.grid(row=0, column=2, padx=5)
# Функция - добавление символа в строку
    def add_symbol(self, digit):
        current_text = self.password_entry.get()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, current_text + digit)
# Функция - удаление символа из строки
    def clear(self):
        self.password_entry.delete(0, tk.END)
# Функция - проверка пароля
    def check_password(self):
        staff_code = self.password_entry.get()
        if not staff_code.isdigit():
            messagebox.showerror("Ошибка", "Пароль должен содержать только цифры.")
            return
        conn = connection_BD()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id_post FROM staff WHERE code = %s", (staff_code,))
                result = cur.fetchone()
                if result:
                    cur.execute("SELECT name_post FROM post WHERE id_post = %s", (result[0],))
                    res = cur.fetchone()
                    if res:
                        if res[0] == 'Управляющая':
                            self.open_manager_window()
                        elif res[0] == 'администратор':
                            self.open_admi_window()
                            self.withdraw()
                        elif res[0] == 'Официант':
                            self.open_off_window()
                        elif res[0] == 'Су-шеф':
                            self.open_shef_window()
                        else:
                            messagebox.showerror("Ошибка", "Неизвестная должность.")
                    else:
                        messagebox.showerror("Ошибка", "Неверный ID сотрудника.")
            except Exception as e:
                messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
            finally:
                conn.close()
# Функция - Открытие окна "Управляющая"
    def open_manager_window(self):
                self.withdraw()
                import manager_window
# Функция - Открытие окна "Шеф"
    def open_shef_window(self):
                self.withdraw()
                import brend_shef
# Функция - Открытие окна "Официант"
    def open_off_window(self):
                self.withdraw()
                import tables
app = In()
app.mainloop()