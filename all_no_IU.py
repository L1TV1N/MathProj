import tkinter as tk
from tkinter import messagebox
from sympy import symbols, sin, cos, integrate, lambdify, sympify
import matplotlib.pyplot as plt
import numpy as np

# Настройка matplotlib
import matplotlib
matplotlib.use("TkAgg")

x = symbols('x')

# === Главное окно ===
root = tk.Tk()
root.title("Интегралы на Python")
root.geometry("800x600")
root.configure(bg="#F0F0F0")

# === Контейнер для всех экранов ===
container = tk.Frame(root)
container.pack(fill="both", expand=True)

frames = {}  # для хранения фреймов

# === Функция переключения между экранами ===
def show_frame(name):
    for frame in frames.values():
        frame.pack_forget()
    frames[name].pack(fill="both", expand=True)

# === Главное меню ===
menu_frame = tk.Frame(container, bg="#FFFFFF")

tk.Label(menu_frame, text="Интегралы на Python", font=("Arial", 24), bg="#FFFFFF").pack(pady=40)
tk.Button(menu_frame, text="📘 Решить пример №20", font=("Arial", 16), width=30, command=lambda: show_frame("example20")).pack(pady=10)
tk.Button(menu_frame, text="🧠 Решить свой интеграл", font=("Arial", 16), width=30, command=lambda: show_frame("custom")).pack(pady=10)
tk.Label(menu_frame, text="https://t.me/L1TV1N4", font=("Arial", 10), bg="#FFFFFF", fg="#888888").pack(side="bottom", pady=10)

# === Экран: Пример 20 ===
example20_frame = tk.Frame(container, bg="#FFFFFF")

tk.Label(example20_frame, text="✅ Пример №20: sin²(3x)", font=("Arial", 20), bg="#FFFFFF").pack(pady=20)

tk.Label(example20_frame, text="Нижний предел (a):", bg="#FFFFFF").pack()
a20_entry = tk.Entry(example20_frame)
a20_entry.insert(0, "0")
a20_entry.pack()

tk.Label(example20_frame, text="Верхний предел (b):", bg="#FFFFFF").pack()
b20_entry = tk.Entry(example20_frame)
b20_entry.insert(0, "3.1416")
b20_entry.pack()

res20_entry = tk.Entry(example20_frame, width=40)
res20_entry.pack(pady=10)

def solve_example_20():
    try:
        a = float(a20_entry.get())
        b = float(b20_entry.get())
        expr = sin(3*x)**2
        reduced_expr = (1 - cos(6*x)) / 2
        result = integrate(reduced_expr, (x, a, b))

        res20_entry.delete(0, "end")
        res20_entry.insert(0, f"Результат: {result.evalf()}")

        f = lambdify(x, expr, 'numpy')
        x_vals = np.linspace(a, b, 400)
        y_vals = f(x_vals)

        plt.figure(figsize=(8, 4))
        plt.plot(x_vals, y_vals, label=r"$\sin^2(3x)$", color="blue")
        plt.fill_between(x_vals, y_vals, alpha=0.3, color='lightblue')
        plt.title(f"График sin²(3x) на [{a}, {b}]")
        plt.grid(True)
        plt.legend()
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

tk.Button(example20_frame, text="Вычислить и построить график", command=solve_example_20).pack(pady=10)
tk.Button(example20_frame, text="⬅ Назад в меню", command=lambda: show_frame("menu")).pack()

# === Экран: Пользовательский интеграл ===
custom_frame = tk.Frame(container, bg="#FFFFFF")

tk.Label(custom_frame, text="🧠 Свой интеграл", font=("Arial", 20), bg="#FFFFFF").pack(pady=20)

tk.Label(custom_frame, text="Функция f(x):", bg="#FFFFFF").pack()
expr_entry = tk.Entry(custom_frame)
expr_entry.insert(0, "sin(x)")
expr_entry.pack()

tk.Label(custom_frame, text="Нижний предел (a):", bg="#FFFFFF").pack()
a_entry = tk.Entry(custom_frame)
a_entry.insert(0, "0")
a_entry.pack()

tk.Label(custom_frame, text="Верхний предел (b):", bg="#FFFFFF").pack()
b_entry = tk.Entry(custom_frame)
b_entry.insert(0, "pi")
b_entry.pack()

res_entry = tk.Entry(custom_frame, width=40)
res_entry.pack(pady=10)

def solve_custom_integral():
    try:
        a = float(a_entry.get())
        b = float(b_entry.get())
        expr_text = expr_entry.get()
        expr = sympify(expr_text)

        result = integrate(expr, (x, a, b))
        res_entry.delete(0, "end")
        res_entry.insert(0, f"Результат: {result.evalf()}")

        f = lambdify(x, expr, 'numpy')
        x_vals = np.linspace(a, b, 400)
        y_vals = f(x_vals)

        plt.figure(figsize=(8, 4))
        plt.plot(x_vals, y_vals, label=f"${expr_text}$", color="green")
        plt.fill_between(x_vals, y_vals, alpha=0.3, color='lightgreen')
        plt.title(f"График {expr_text} на отрезке [{a}, {b}]")
        plt.grid(True)
        plt.legend()
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

tk.Button(custom_frame, text="Вычислить и построить график", command=solve_custom_integral).pack(pady=10)
tk.Button(custom_frame, text="⬅ Назад в меню", command=lambda: show_frame("menu")).pack()

# === Регистрация фреймов ===
frames["menu"] = menu_frame
frames["example20"] = example20_frame
frames["custom"] = custom_frame

# Показываем меню при старте
show_frame("menu")

root.mainloop()
