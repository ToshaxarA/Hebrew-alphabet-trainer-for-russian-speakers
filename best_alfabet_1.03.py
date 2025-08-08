import random
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Полный алфавит с софитами + дубликаты для "строчных"
HEBREW = [
    ("א", "алеф", "нет звука / 'а'", "alef.png"),
    ("ב", "бет", "б / в", "bet.png"),
    ("ג", "гимел", "г", "gimel.png"),
    ("ד", "далет", "д", "dalet.png"),
    ("ה", "хэй", "х / 'h'", "hey.png"),
    ("ו", "вав", "в / у", "vav.png"),
    ("ז", "заин", "з", "zayin.png"),
    ("ח", "хет", "х", "chet.png"),
    ("ט", "тет", "т", "tet.png"),
    ("י", "йод", "й / и", "yod.png"),
    ("כ", "каф", "к", "kaf.png"),
    ("ך", "каф софит", "к", "kaf_sofit.png"),
    ("ל", "ламед", "л", "lamed.png"),
    ("מ", "мем", "м", "mem.png"),
    ("ם", "мем софит", "м", "mem_sofit.png"),
    ("נ", "нун", "н", "nun.png"),
    ("ן", "нун софит", "н", "nun_sofit.png"),
    ("ס", "самех", "с", "samekh.png"),
    ("ע", "айн", "нет звука / 'а'", "ayin.png"),
    ("פ", "пей", "п / ф", "pey.png"),
    ("ף", "пей софит", "п / ф", "pey_sofit.png"),
    ("צ", "цади", "ц", "tsadi.png"),
    ("ץ", "цади софит", "ц", "tsadi_sofit.png"),
    ("ק", "куф", "к", "kuf.png"),
    ("ר", "реш", "р", "resh.png"),
    ("ש", "шин", "ш / с", "shin.png"),
    ("ת", "тав", "т", "tav.png"),
]

# Дубликаты для "строчных" (визуально одинаковы, но для тренировки)
HEBREW += [(l.lower(), name + " (строчная)", sound, img) for l, name, sound, img in HEBREW]


class HebrewTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажёр алфавита иврита")
        self.root.geometry("600x600")

        # Озвучка
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        # Статистика
        self.correct = 0
        self.total = 0

        # Элементы интерфейса
        self.setup_ui()

        # Показать первую букву
        self.next_letter()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            self.main_frame,
            text="Тренажёр алфавита иврита",
            font=('Helvetica', 20, 'bold'),
            bootstyle=PRIMARY
        ).pack(pady=10)

        self.image_label = ttk.Label(self.main_frame)
        self.image_label.pack(pady=10)

        self.letter_label = ttk.Label(
            self.main_frame,
            text="",
            font=('Helvetica', 40, 'bold'),
            bootstyle=INFO
        )
        self.letter_label.pack(pady=10)

        self.entry = ttk.Entry(self.main_frame, font=('Helvetica', 14))
        self.entry.pack(pady=5)

        self.check_button = ttk.Button(
            self.main_frame,
            text="Проверить",
            bootstyle=SUCCESS,
            command=self.check_answer
        )
        self.check_button.pack(pady=5)

        self.sound_button = ttk.Button(
            self.main_frame,
            text="🔊 Озвучить",
            bootstyle=SECONDARY,
            command=self.say_letter
        )
        self.sound_button.pack(pady=5)

        self.score_label = ttk.Label(
            self.main_frame,
            text="Правильно: 0 | Всего: 0",
            font=('Helvetica', 12),
            bootstyle=SECONDARY
        )
        self.score_label.pack(pady=10)

        # Подпись разработчика
        ttk.Label(
            self.main_frame,
            text="Разработчик Антон Харчевский",
            font=('Helvetica', 14),
            bootstyle=SECONDARY
        ).pack(side=tk.BOTTOM, anchor='se', pady=5, padx=10)

    def next_letter(self):
        self.current_letter = random.choice(HEBREW)
        letter, name, sound, image_file = self.current_letter
        self.letter_label.config(text=letter)

        if os.path.exists(image_file):
            img = Image.open(image_file)
            img = img.resize((150, 150))
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
        else:
            self.image_label.config(image="", text="(Нет картинки)")

        self.entry.delete(0, tk.END)

    def check_answer(self):
        answer = self.entry.get().strip().lower()
        correct_answer = self.current_letter[1].lower()

        self.total += 1
        if answer == correct_answer:
            self.correct += 1
            messagebox.showinfo("Правильно!", "Отличная работа!")
        else:
            messagebox.showerror("Ошибка", f"Правильный ответ: {self.current_letter[1]}")

        self.update_score()
        self.next_letter()

    def update_score(self):
        self.score_label.config(text=f"Правильно: {self.correct} | Всего: {self.total}")

    def say_letter(self):
        self.engine.say(self.current_letter[0])
        self.engine.runAndWait()


if __name__ == "__main__":
    root = ttk.Window(themename="minty")
    app = HebrewTrainer(root)
    root.mainloop()
