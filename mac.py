import tkinter as tk
from tkinter import Canvas, Entry, Button, Text, PhotoImage, messagebox
from pathlib import Path
from sympy import symbols, sin, cos, integrate, lambdify, sympify
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

x = symbols('x')

# === Масштабирование ===
scale = 0.7
def s(val): return int(val * scale)  # масштаб координат и размеров
def fs(val): return int(val * scale)  # масштаб шрифта

# === Пути к ресурсам ===
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "build/assets"

def relative_to_assets(frame: str, path: str) -> Path:
    return ASSETS_PATH / frame / path

# === Главное окно ===
root = tk.Tk()
root.geometry(f"{s(1280)}x{s(800)}")
root.configure(bg="#3a3939")
root.title("Интегралы на Python")

# === Контейнер для фреймов ===
container = tk.Frame(root, bg="#3a3939")
container.pack(fill="both", expand=True)

frames = {}

# === Переключение между фреймами ===
def show_frame(name):
    for f in frames.values():
        f.pack_forget()
    frames[name].pack(fill="both", expand=True)

# === Главное меню ===
menu_frame = tk.Frame(container, bg="#3a3939")
canvas0 = Canvas(menu_frame, bg="#3a3939", height=s(800), width=s(1280), bd=0, highlightthickness=0, relief="ridge")
canvas0.place(x=0, y=0)

img_bg_0 = PhotoImage(file=relative_to_assets("frame0", "image_1.png"))
canvas0.create_image(s(667), s(445), image=img_bg_0)
canvas0.create_text(s(261), s(89), anchor="nw", text="Интегралы на python", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-60)))
canvas0.create_text(s(1085), s(780), anchor="nw", text="https://t.me/L1TV1N4", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-15)))

# === Кнопки главного меню ===
img_btn_1 = PhotoImage(file=relative_to_assets("frame0", "button_3.png"))
img_btn_2 = PhotoImage(file=relative_to_assets("frame0", "button_1.png"))
img_btn_3 = PhotoImage(file=relative_to_assets("frame0", "button_2.png"))

def create_rounded_image_button(parent, x, y, width, height, radius, image: PhotoImage, command, bg_color="#4CAF50"):
    canvas = Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, bd=0)
    canvas.place(x=x, y=y)

    # Закруглённый прямоугольник
    canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((width-radius*2, 0, width, radius*2), start=0, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((0, height-radius*2, radius*2, height), start=180, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((width-radius*2, height-radius*2, width, height), start=270, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_rectangle((radius, 0, width - radius, height), fill=bg_color, outline=bg_color)
    canvas.create_rectangle((0, radius, width, height - radius), fill=bg_color, outline=bg_color)

    # PNG поверх кнопки
    image_obj = canvas.create_image(width // 2, height // 2, image=image)
    canvas.tag_bind(image_obj, "<Button-1>", lambda e: command())
    canvas.bind("<Button-1>", lambda e: command())

    return canvas

create_rounded_image_button(menu_frame, x=s(424), y=s(295), width=s(433), height=s(85), radius=s(30), image=img_btn_1, command=lambda: show_frame("example20"))
create_rounded_image_button(menu_frame, x=s(424), y=s(419), width=s(433), height=s(85), radius=s(30), image=img_btn_2, command=lambda: show_frame("custom"))
create_rounded_image_button(menu_frame, x=s(424), y=s(539), width=s(433), height=s(85), radius=s(30), image=img_btn_3, command=lambda: show_frame("neuro"))
# === Пример №20 ===
example20_frame = tk.Frame(container, bg="#3a3939")
canvas1 = Canvas(example20_frame, bg="#3a3939", height=s(800), width=s(1280), bd=0, highlightthickness=0, relief="ridge")
canvas1.place(x=0, y=0)

canvas1.create_text(s(240), s(89), anchor="nw", text="✅ Решить пример №20", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-60)))
canvas1.create_text(s(1085), s(780), anchor="nw", text="https://t.me/L1TV1N4", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-15)))

canvas1.create_text(s(525), s(315), anchor="nw", text="Нижний предел (а):", fill="#FFFFFF", font=("SFProText Medium", fs(12)))
canvas1.create_text(s(525), s(364), anchor="nw", text="Верхний предел (b):", fill="#FFFFFF", font=("SFProText Medium", fs(12)))
canvas1.create_text(s(525), s(469), anchor="nw", text="Результат:", fill="#FFFFFF", font=("SFProText Medium", fs(12)))

image_example20_bg = PhotoImage(file=relative_to_assets("frame1", "image_2.png"))
canvas1.create_image(s(639), s(267), image=image_example20_bg)

entry_1 = Entry(example20_frame, bd=0, bg="#9B9B9B", fg="#000716")
entry_1.place(x=s(528), y=s(335), width=s(223), height=s(26))
entry_1.insert(0, "0")

entry_2 = Entry(example20_frame, bd=0, bg="#9B9B9B", fg="#000716")
entry_2.place(x=s(528), y=s(390), width=s(223), height=s(26))
entry_2.insert(0, "3.14")

entry_3 = Entry(example20_frame, bd=0, bg="#9B9B9B", fg="#000716")
entry_3.place(x=s(528), y=s(486), width=s(223), height=s(26))

def solve_example_20():
    try:
        a = float(entry_1.get())
        b = float(entry_2.get())
        expr = sin(3 * x) ** 2
        result = integrate((1 - cos(6 * x)) / 2, (x, a, b))
        entry_3.delete(0, "end")
        entry_3.insert(0, str(result.evalf()))

        f = lambdify(x, expr, 'numpy')
        x_vals = np.linspace(a, b, 400)
        y_vals = f(x_vals)

        plt.figure(figsize=(7, 3.5))
        plt.plot(x_vals, y_vals, label=r"$\sin^2(3x)$", color="blue")
        plt.fill_between(x_vals, y_vals, alpha=0.3)
        plt.grid(True)
        plt.legend()
        plt.title("График sin²(3x)", color="white")
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

btn_calc1_img = PhotoImage(file=relative_to_assets("frame1", "button_1.png"))
btn_calc1 = Button(example20_frame, image=btn_calc1_img, borderwidth=0, highlightthickness=0, command=solve_example_20, relief="flat")
btn_calc1.place(x=s(522), y=s(431), width=s(235), height=s(28))

btn_back1_img = PhotoImage(file=relative_to_assets("frame1", "button_2.png"))
btn_back1 = Button(example20_frame, image=btn_back1_img, borderwidth=0, highlightthickness=0, command=lambda: show_frame("menu"), relief="flat")
btn_back1.place(x=s(54), y=s(27), width=s(73), height=s(26))
# === Свой интеграл ===
custom_frame = tk.Frame(container, bg="#3a3939")
canvas2 = Canvas(custom_frame, bg="#3a3939", height=s(800), width=s(1280), bd=0, highlightthickness=0, relief="ridge")
canvas2.place(x=0, y=0)

canvas2.create_text(s(200), s(70), anchor="nw", text="🧠 Решить свой интеграл", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-60)))
canvas2.create_text(s(1085), s(780), anchor="nw", text="https://t.me/L1TV1N4", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-15)))

canvas2.create_text(s(480), s(200), anchor="nw", text="Функция f(x):", fill="#FFFFFF", font=("SFProText Medium", fs(14)))
canvas2.create_text(s(480), s(235), anchor="nw", text="Python стиль: sin(x), cos(x), exp(x), x**2", fill="#AFAFAF", font=("SFProText Medium", fs(10)))
canvas2.create_text(s(480), s(290), anchor="nw", text="Нижний предел (a):", fill="#FFFFFF", font=("SFProText Medium", fs(12)))
canvas2.create_text(s(480), s(340), anchor="nw", text="Верхний предел (b):", fill="#FFFFFF", font=("SFProText Medium", fs(12)))
canvas2.create_text(s(480), s(445), anchor="nw", text="Результат:", fill="#FFFFFF", font=("SFProText Medium", fs(12)))

image_custom_bg = PhotoImage(file=relative_to_assets("frame2", "image_2.png"))
canvas2.create_image(s(380), s(252), image=image_custom_bg)

entry_fx = Entry(custom_frame, bd=0, bg="#9B9B9B", fg="#000716")
entry_fx.place(x=s(620), y=s(200), width=s(250), height=s(26))
entry_fx.insert(0, "sin(x)")

entry_a = Entry(custom_frame, bd=0, bg="#9B9B9B", fg="#000716")
entry_a.place(x=s(620), y=s(290), width=s(100), height=s(26))
entry_a.insert(0, "0")

entry_b = Entry(custom_frame, bd=0, bg="#9B9B9B", fg="#000716")
entry_b.place(x=s(620), y=s(340), width=s(100), height=s(26))
entry_b.insert(0, "3.14")

entry_result = Entry(custom_frame, bd=0, bg="#9B9B9B", fg="#000716")
entry_result.place(x=s(620), y=s(445), width=s(250), height=s(26))

def solve_custom():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        expr = sympify(entry_fx.get())
        result = integrate(expr, (x, a, b))
        entry_result.delete(0, "end")
        entry_result.insert(0, str(result.evalf()))

        f = lambdify(x, expr, 'numpy')
        x_vals = np.linspace(a, b, 400)
        y_vals = f(x_vals)

        plt.figure(figsize=(7, 3.5))
        plt.plot(x_vals, y_vals, label=str(expr), color="green")
        plt.fill_between(x_vals, y_vals, alpha=0.3)
        plt.grid(True)
        plt.legend()
        plt.title("График пользовательской функции", color="white")
        plt.show()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

btn_calc2_img = PhotoImage(file=relative_to_assets("frame2", "button_1.png"))
btn_calc2 = Button(custom_frame, image=btn_calc2_img, borderwidth=0, highlightthickness=0, command=solve_custom, relief="flat")
btn_calc2.place(x=s(502), y=s(521), width=s(237), height=s(28))

btn_back2_img = PhotoImage(file=relative_to_assets("frame2", "button_2.png"))
btn_back2 = Button(custom_frame, image=btn_back2_img, borderwidth=0, highlightthickness=0, command=lambda: show_frame("menu"), relief="flat")
btn_back2.place(x=s(54), y=s(27), width=s(73), height=s(26))


# === Нейросеть ===
neuro_frame = tk.Frame(container, bg="#3a3939")
canvas3 = Canvas(neuro_frame, bg="#3a3939", height=s(800), width=s(1280), bd=0, highlightthickness=0, relief="ridge")
canvas3.place(x=0, y=0)

canvas3.create_text(s(200), s(50), anchor="nw", text="🤖 Спросить у нейросети", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-60)))
canvas3.create_text(s(1085), s(780), anchor="nw", text="https://t.me/L1TV1N4", fill="#FFFFFF", font=("GetVoIPGrotesque", fs(-15)))

btn_back3 = Button(neuro_frame, text="⬅ Назад", font=("Arial", fs(12)), command=lambda: show_frame("menu"), fg="#FFFFFF", bg="#3a3939")
btn_back3.place(x=s(54), y=s(27), width=s(73), height=s(26))

chat_output = Text(neuro_frame, wrap="word", bg="#2e2e2e", fg="white", font=("Arial", fs(12)))
chat_output.place(x=s(100), y=s(140), width=s(1080), height=s(500))

chat_input = Entry(neuro_frame, bd=0, bg="#9B9B9B", fg="#FFFFFF", font=("Arial", fs(12)))
chat_input.place(x=s(100), y=s(660), width=s(880), height=s(30))

giga = GigaChat(
    credentials="ZDAzN2RjODYtMDBhZi00ZGNhLWJhYWYtODk4MDM0Njg5NzA2OjQ1N2NhYjRjLTNhNGMtNDc3OS05MmI2LTk1YzJlY2E3MTBhMw==",
    verify_ssl_certs=False,
    temperature=0.7,
    model="GigaChat",
    scope="GIGACHAT_API_PERS",
)

messages = [SystemMessage(content="Ты дружелюбный и умный помощник в высшей математике. Отвечай только на темы связанные с математикой на русском языке чётко и по делу.")]

def send_to_neuro():
    user_text = chat_input.get().strip()
    if not user_text:
        return
    chat_output.insert("end", f"\nВы: {user_text}\n")
    chat_input.delete(0, "end")
    try:
        messages.append(HumanMessage(content=user_text))
        res = giga.invoke(messages)
        messages.append(res)
        chat_output.insert("end", f"🤖 : {res.content}\n")
        chat_output.see("end")
    except Exception as e:
        chat_output.insert("end", f"[Ошибка] {str(e)}\n")
        chat_output.see("end")

btn_send = Button(neuro_frame, text="Отправить", font=("Arial", fs(12)), command=send_to_neuro, bg="#4CAF50", fg="white")
btn_send.place(x=s(1000), y=s(670), width=s(180), height=s(30))

# === Регистрация фреймов и запуск ===
frames["menu"] = menu_frame
frames["example20"] = example20_frame
frames["custom"] = custom_frame
frames["neuro"] = neuro_frame

show_frame("menu")
root.resizable(False, False)
root.mainloop()
