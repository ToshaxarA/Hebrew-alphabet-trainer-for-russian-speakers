"""
Hebrew Alphabet Trainer - Final Perfect Version
- Все кнопки РАЗНЫХ цветов (гарантированно)
- Буква всегда по центру
- Округлые кнопки ответов
- Кнопки расположены выше
- Красивый дизайн
- Отображение результата (правильно/неправильно) исправлено
"""

import random
import os
import sys # Добавлено для работы с PyInstaller
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import pygame

# Функция для определения пути к файлам в PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Инициализация звука
pygame.mixer.init()

# Яркие контрастные цвета для кнопок
# Note: These colors are used to dynamically create ttk styles, as setting
# the 'bg' attribute directly on a ttk.Button is not supported.
BUTTON_COLORS = [
    '#007BFF', '#28A745', '#DC3545', '#FFC107',
    '#17A2B8', '#6F42C1', '#FD7E14', '#E83E8C',
    '#6C757D', '#20C997', '#FF9800', '#6A1B9A'
]

# Размеры шрифтов
TITLE_FONT = ('Helvetica', 36, 'bold')
QUESTION_FONT = ('Helvetica', 120, 'bold')
# Изменение: размер шрифта для кнопок ответов увеличен с 24 до 36
ANSWER_FONT = ('Helvetica', 36, 'bold')
ACTION_FONT = ('Helvetica', 18, 'bold')
SCORE_FONT = ('Helvetica', 24, 'bold')
MODE_FONT = ('Helvetica', 18, 'bold')
RESULT_FONT = ('Helvetica', 42, 'bold')

# Данные букв
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

class HebrewTrainer:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(theme='lumen') # Обновлено: новая тема 'lumen'
        
        # Настройка стилей
        self.style.configure('Action.TButton', font=ACTION_FONT)
        self.style.configure('Radio.TRadiobutton', font=MODE_FONT)
        self.style.configure('Title.TLabel', font=TITLE_FONT)
        self.style.configure('Question.TLabel', font=QUESTION_FONT)
        self.style.configure('Score.TLabel', font=SCORE_FONT)
        self.style.configure('Result.TLabel', font=RESULT_FONT)
        self.style.configure('Developer.TLabel', font=('Helvetica', 10, 'bold'), foreground='grey')

        # Создаем стили для кнопок ответов с разными цветами
        self.button_styles = []
        for i, color in enumerate(BUTTON_COLORS):
            style_name = f'Custom{i}.TButton'
            self.style.configure(style_name,
                                 background=color,
                                 foreground='white',
                                 font=ANSWER_FONT,
                                 padding=(20, 20),
                                 bordercolor='black', # Изменено: добавлен чёрный контур
                                 borderwidth=2,       # Изменено: увеличена толщина контура
                                 focuscolor='black')  # Изменено: цвет контура при фокусе также чёрный
            self.style.map(style_name,
                           background=[('active', self.darken_color(color))],
                           foreground=[('active', 'white')])
            self.button_styles.append(style_name)

        self.root.title("Hebrew Trainer")
        self.root.geometry("1200x900")
        
        # Проверка звуковых файлов
        self.sounds_available = True
        # Обновлено: теперь используется resource_path
        if not os.path.exists(resource_path("right1.mp3")):
            print("Файл right1.mp3 не найден")
            self.sounds_available = False
        # Обновлено: теперь используется resource_path
        if not os.path.exists(resource_path("false1.mp3")):
            print("Файл false1.mp3 не найден")
            self.sounds_available = False
        
        self.current_letter = None
        self.score = 0
        self.total = 0
        self.mode = 'letter_to_name'
        
        self.setup_ui()
        self.new_question()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH)
        
        # Заголовок
        ttk.Label(
            self.main_frame, 
            text="Тренажёр алфавита иврита", 
            style='Title.TLabel',
            bootstyle=PRIMARY
        ).pack(pady=10)
        
        # Переключатель режимов
        mode_frame = ttk.Frame(self.main_frame)
        mode_frame.pack(pady=10)
        
        self.mode_var = tk.StringVar(value=self.mode)
        ttk.Radiobutton(
            mode_frame, 
            text="Буква → Название", 
            variable=self.mode_var,
            value='letter_to_name',
            command=self.change_mode,
            bootstyle="toolbutton",
            style='Radio.TRadiobutton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            mode_frame, 
            text="Название → Буква", 
            variable=self.mode_var,
            value='name_to_letter',
            command=self.change_mode,
            bootstyle="toolbutton",
            style='Radio.TRadiobutton'
        ).pack(side=tk.LEFT, padx=10)
        
        # Центральная область с вопросом и результатом
        self.center_frame = ttk.Frame(self.main_frame)
        self.center_frame.pack(fill=tk.X, pady=(0, 0)) 
        
        # Область вопроса (по центру)
        self.question_label = ttk.Label(
            self.center_frame,
            style='Question.TLabel',
            bootstyle=PRIMARY,
            anchor=tk.CENTER
        )
        self.question_label.pack(fill=tk.X)
        
        # Область результата (под вопросом)
        self.result_label = ttk.Label(
            self.center_frame,
            text="",
            font=RESULT_FONT,
            bootstyle=SECONDARY,
            anchor=tk.CENTER
        )
        self.result_label.pack(fill=tk.X, pady=(5, 0))
        
        # Область ответов (высокие кнопки)
        self.answers_frame = ttk.Frame(self.main_frame)
        self.answers_frame.pack(fill=tk.X, pady=(0, 0)) 
        
        # Панель действий
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        # Кнопка "Подсказка" удалена
        
        ttk.Button(
            action_frame,
            text="Следующий",
            command=self.new_question,
            bootstyle=(OUTLINE, INFO),
            style='Action.TButton',
        ).pack(side=tk.RIGHT, padx=10, ipady=5)
        
        # Счет
        self.score_label = ttk.Label(
            self.main_frame,
            text="Правильно: 0 | Всего: 0",
            style='Score.TLabel',
            bootstyle=SECONDARY
        )
        self.score_label.pack(pady=10)
         # Метка "Разработчик" в правом нижнем углу
        self.dev_label = tk.Label(
            self.root,
            text="Разработчик Антон Харчевский",
            font=('Helvetica', 10, 'bold'),
            fg='#808080',  # Серый цвет
            bg='#f0f0f0',  # Цвет фона (можно сделать его прозрачным, используя opacity, но это сложнее)
            bd=0,  # Убираем рамку
            relief=tk.FLAT
        )
        self.dev_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')
    
    def change_mode(self):
        self.mode = self.mode_var.get()
        self.score = 0
        self.total = 0
        self.update_score()
        self.new_question()
    
    def new_question(self):
        self.result_label.config(text="")
        
        self.current_letter = random.choice(HEBREW)
        
        for widget in self.answers_frame.winfo_children():
            widget.destroy()
        
        if self.mode == 'letter_to_name':
            self.question_label.config(text=self.current_letter[0])
            options = self.generate_options('name')
        else:
            text = f"{self.current_letter[1]}\n({self.current_letter[2]})"
            self.question_label.config(text=text, font=('Helvetica', 48, 'bold'))
            options = self.generate_options('letter')
        
        styles_for_buttons = random.sample(self.button_styles, 4)
        for option, style_name in zip(options, styles_for_buttons):
            btn = ttk.Button(
                self.answers_frame,
                text=option,
                command=lambda o=option: self.check_answer(o),
                style=style_name
            )
            btn.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.X)
    
    def darken_color(self, color, factor=0.7):
        r = int(int(color[1:3], 16) * factor)
        g = int(int(color[3:5], 16) * factor)
        b = int(int(color[5:7], 16) * factor)
        return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"
    
    def generate_options(self, target):
        if target == 'name':
            correct = self.current_letter[1]
            idx = 1
        else:
            correct = self.current_letter[0]
            idx = 0
        
        options = [correct]
        while len(options) < 4:
            candidate = random.choice(HEBREW)[idx]
            if candidate not in options:
                options.append(candidate)
        
        random.shuffle(options)
        return options
    
    def check_answer(self, answer):
        self.total += 1
        correct = False
        
        if self.mode == 'letter_to_name':
            correct = (answer == self.current_letter[1])
        else:
            correct = (answer == self.current_letter[0])
        
        if self.sounds_available:
            sound_file = "right1.mp3" if correct else "false1.mp3"
            try:
                # Обновлено: теперь используется resource_path
                pygame.mixer.Sound(resource_path(sound_file)).play()
            except Exception as e:
                print(f"Ошибка при воспроизведении звука: {e}")
        
        if correct:
            self.score += 1
            self.show_result("✓ Правильно!", "success")
        else:
            correct_answer = f"{self.current_letter[0]} — {self.current_letter[1]}" if self.mode == 'letter_to_name' else self.current_letter[0]
            self.show_result(f"✗ Неверно! Правильно: {correct_answer}", "danger")
        
        self.update_score()
        self.root.after(1500, self.new_question)
    
    def show_result(self, message, style):
        self.result_label.config(text=message, bootstyle=style, font=RESULT_FONT)
    
    def update_score(self):
        self.score_label.config(text=f"Правильно: {self.score} | Всего: {self.total}")
    
    # Метод show_hint был полностью удален
    
if __name__ == "__main__":
    root = ttk.Window(themename="lumen") # Обновлено: новая тема 'lumen'
    app = HebrewTrainer(root)
    root.mainloop()
