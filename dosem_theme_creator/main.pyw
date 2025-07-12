import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog, Toplevel
import json
from PIL import Image, ImageTk
import os

# Этот инструмент дает возможность более простым способом создать кастомную тему для терминала. 
# В будующем постараюсь сделать это еще проще

class ThemeCreator: # Основной класс
    def __init__(self, root): # Конструктор полей
        self.root = root
        self.root.title("DOSem Theme Creator") # Название окна
        self.root.geometry("700x550") # Изначальный размер окна
        self.root.minsize(700, 550) # Минимальный размер окна

        # Абсолютный путь к папке проекта
        self.project_path = os.path.dirname(os.path.abspath(__file__))

        # Локализации
        self.languages = { # Текст локализации. Очень огромный.
            "ru": {
                "file_menu": "Файл",
                "new_theme": "Новая тема",
                "exit": "Выход",
                "options_menu": "Опции",
                "language": "Язык",
                "english": "Английский",
                "russian": "Русский",
                "help_menu": "Справка",
                "help": "Помощь",
                "steps_title": "Шаги создания темы",
                "steps": [
                    "Введите название темы:",
                    "Выберите цвет фона (bg_color):",
                    "Выберите цвет текста (text_color):",
                    "Выберите цвет выделения (selection_bg):",
                    "Выберите цвет для 'system' текста:",
                    "Выберите цвет для 'error' текста:",
                    "Выберите цвет для 'success' текста:",
                    "Выберите цвет для 'info' текста:",
                    "Выберите цвет для 'command' текста:",
                    "Выберите цвет для 'output' текста:"
                ],
                "main_text": "Создайте новую тему: Файл -> Новая тема",
                "color_btn": "Выбрать цвет",
                "back_btn": "←",
                "next_btn": "→",
                "save_btn": "Сохранить тему",
                "error_title": "Ошибка",
                "name_error": "Введите название темы!",
                "color_error": "Выберите цвет!",
                "all_colors_error": "Выберите все необходимые цвета!",
                "fields_error": "Не все поля темы заполнены!",
                "success_title": "Успех",
                "success_msg": "Тема '{}' успешно сохранена!\n\nЧтобы добавить её в DOSem, извлеките содержимое файла в словарь THEMES в DOSem.\nПодробнее в 'справка'",
                "save_error": "Не удалось сохранить файл:\n{}",
                "help_text": """Инструкция по созданию темы:

1. Начните создание новой темы через меню Файл -> Новая тема
2. Введите название темы
3. Последовательно заполните все необходимые цвета:
   - Фон основного окна
   - Цвет текста
   - Цвет выделения
   - Цвета для различных типов текста (системные сообщения, ошибки и т.д.)
   
Как добавить тему после получения JSON:
"""
            },
            "en": {
                "file_menu": "File",
                "new_theme": "New theme",
                "exit": "Exit",
                "options_menu": "Options",
                "language": "Language",
                "english": "English",
                "russian": "Russian",
                "help_menu": "Help",
                "help": "Help",
                "steps_title": "Theme creation steps",
                "steps": [
                    "Enter theme name:",
                    "Select background color (bg_color):",
                    "Select text color (text_color):",
                    "Select highlight color (selection_bg):",
                    "Select color for 'system' text:",
                    "Select color for 'error' text:",
                    "Select color for 'success' text:",
                    "Select color for 'info' text:",
                    "Select color for 'command' text:",
                    "Select color for 'output' text:"
                ],
                "main_text": "Create a new theme: File -> New theme",
                "color_btn": "Choose color",
                "back_btn": "←",
                "next_btn": "→",
                "save_btn": "Save theme",
                "error_title": "Error",
                "name_error": "Enter theme name!",
                "color_error": "Choose color!",
                "all_colors_error": "Choose all required colors!",
                "fields_error": "Not all theme fields are filled!",
                "success_title": "Success",
                "success_msg": "Theme '{}' saved successfully!\n\nTo use it in DOSem, cut the file content and past\nto the THEMES dictionary in DOSem.",
                "save_error": "Failed to save file:\n{}",
                "help_text": """Theme creation guide:

1. Start new theme creation via File -> New theme
2. Enter theme name
3. Enter all required colors step by step:
   - Main window background
   - Text color
   - Highlight color
   - Colors for different text types (system messages, errors etc.)
   
How to add after compilation:
"""
            }
        }
        # Текущий язык
        self.current_lang = "en"

        # Каркас для создания темы, который будет постепенно заполнятся
        self.theme_data = { 
            "name": "",
            "bg_color": "",
            "text_color": "",
            "selection_bg": "",
            "tags": {
                "system": "",
                "error": "",
                "success": "",
                "info": "",
                "command": "",
                "output": ""
            }
        }

        self.steps = self.languages[self.current_lang]["steps"]
        self.current_step = 0 # При создании новой темы, шаги обновляются
        self.creating_theme = False # По умолчанию естественно False

        # Пути к изображениям для справки 
        self.help_images = [
            os.path.join(self.project_path, "step1.png"),
            os.path.join(self.project_path, "step2.png"),
            os.path.join(self.project_path, "step3.png"),
            os.path.join(self.project_path, "step4.png")
        ]

        # Создаем интерфейс
        self.create_menu() # Маунтим меню
        self.create_widgets()
        self.show_initial_screen()
        
    def create_menu(self): # Функция создания меню
        # Главное меню
        menubar = tk.Menu(self.root) # Создаем панельку
    
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0) 
        file_menu.add_command(label=self.languages[self.current_lang]["new_theme"], command=self.start_new_theme)
        file_menu.add_separator()
        file_menu.add_command(label=self.languages[self.current_lang]["exit"], command=self.root.quit)
        menubar.add_cascade(label=self.languages[self.current_lang]["file_menu"], menu=file_menu)

        # Меню Опции
        options_menu = tk.Menu(menubar, tearoff=0)
    
        # Подменю языка с динамическими названиями
        lang_menu = tk.Menu(options_menu, tearoff=0)
        lang_menu.add_command(
            label=self.languages[self.current_lang]["english"],
            command=lambda: self.change_language("en")
        )
        lang_menu.add_command(
            label=self.languages[self.current_lang]["russian"],
            command=lambda: self.change_language("ru")
        )
    
        options_menu.add_cascade(
            label=self.languages[self.current_lang]["language"],
            menu=lang_menu
        )
        menubar.add_cascade(
            label=self.languages[self.current_lang]["options_menu"],
            menu=options_menu
        )
    
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label=self.languages[self.current_lang]["help"],
            command=self.show_help
        )
        menubar.add_cascade(
            label=self.languages[self.current_lang]["help_menu"],
            menu=help_menu
        )
    
        self.root.config(menu=menubar)

    def change_language(self, lang): # Функция изменения языка
        self.current_lang = lang
        self.steps = self.languages[lang]["steps"]
    
        # Полностью пересоздаем меню с новыми названиями
        self.create_menu()
    
        # Обновляем остальные элементы интерфейса
        if hasattr(self, 'main_text'):
            if not self.creating_theme:
                self.main_text.config(text=self.languages[lang]["main_text"])
            else:
                # Если идет процесс создания темы, скрываем первоначальный текст
                self.main_text.pack_forget()
    
        if hasattr(self, 'color_btn'):
            self.color_btn.config(text=self.languages[lang]["color_btn"])
        if hasattr(self, 'back_btn'):
            self.back_btn.config(text=self.languages[lang]["back_btn"])
        if hasattr(self, 'next_btn'):
            next_text = self.languages[lang]["next_btn"] if self.current_step < len(self.steps)-1 else self.languages[lang]["save_btn"].split()[0]
            self.next_btn.config(text=next_text)
        if hasattr(self, 'save_btn'):
            self.save_btn.config(text=self.languages[lang]["save_btn"])
    
        # Если идет процесс создания темы, обновляем текущий шаг
        if self.creating_theme and hasattr(self, 'step_label'):
            self.update_step()

    def show_help(self): # Функция окна справки
        help_window = Toplevel(self.root)
        help_window_icon_path = os.path.join(script_dir, "help.ico")
        help_window.title(self.languages[self.current_lang]["help"])
        help_window.geometry("650x600")
        help_window.minsize(650, 600)
        help_window.iconbitmap(help_window_icon_path)
        
        # Основной фрейм с прокруткой
        main_frame = tk.Frame(help_window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Холст и скроллбар
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(
            main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Текст справки
        help_text = tk.Label(
            scrollable_frame,
            text=self.languages[self.current_lang]["help_text"],
            font=('Arial', 10),
            justify=tk.LEFT,
            wraplength=580
        )
        help_text.pack(padx=10, pady=10, anchor="w")

        author_name = tk.Label(
            scrollable_frame,
            text="CD-ROM SOFT",
            font=('Arial', 8),
            justify=tk.CENTER,
            wraplength=50
        )
        author_name.pack(padx=0, pady=10, anchor="w")

        # Загрузка и отображение изображений
        for img_path in self.help_images:
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img.thumbnail((600, 400))
                    photo = ImageTk.PhotoImage(img)

                    img_label = tk.Label(scrollable_frame, image=photo)
                    img_label.image = photo
                    img_label.pack(pady=5)

                    # Подпись к изображению
                    caption = tk.Label(
                        scrollable_frame,
                        text=os.path.basename(img_path),
                        font=('Arial', 8),
                        fg="gray"
                    )
                    caption.pack()
            except Exception as e:
                error_label = tk.Label(
                    scrollable_frame,
                    text=f"Ошибка загрузки {os.path.basename(img_path)}: {str(e)}",
                    fg="red"
                )
                error_label.pack()

    def create_widgets(self): # Функция создания виджетов
        # Основной текст
        self.main_text = tk.Label(
            self.root,
            text=self.languages[self.current_lang]["main_text"],
            font=('Arial', 14),
            pady=20
        )
        self.main_text.pack(expand=True)

        # Текст шага
        self.step_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 12),
            pady=10
        )

        # Поле ввода (для названия темы)
        self.entry_frame = tk.Frame(self.root)
        self.entry = tk.Entry(self.entry_frame, font=('Arial', 12), width=30)
        self.entry.pack(side=tk.LEFT, padx=5)

        # Кнопка выбора цвета
        self.color_btn = tk.Button(
            self.entry_frame,
            text=self.languages[self.current_lang]["color_btn"],
            command=self.choose_color
        )
        self.color_btn.pack(side=tk.LEFT, padx=5)

        # Кнопки навигации
        self.nav_frame = tk.Frame(self.root)
        
        # Кнопка "Назад"
        self.back_btn = tk.Button(
            self.nav_frame,
            text="←",
            font=('Arial', 14, 'bold'),
            command=self.prev_step,
            state=tk.DISABLED,
            width=3,
            padx=5
        )
        self.back_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка далее
        self.next_btn = tk.Button(
            self.nav_frame,
            text="→",
            font=('Arial', 14, 'bold'),
            command=self.next_step,
            width=3,
            padx=5
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Образец текста
        self.preview_frame = tk.Frame(self.root)
        self.preview_labels = []

        # Кнопка сохранения
        self.save_btn = tk.Button(
            self.root,
            text=self.languages[self.current_lang]["save_btn"],
            command=self.save_theme,
            state=tk.DISABLED
        )

    def show_initial_screen(self): # Функция показывания первоначального экрана
        self.creating_theme = False # Ставим флаг на то, что в самом начале мы не создаем тему.
        self.main_text.pack(expand=True)
        self.step_label.pack_forget()
        self.entry_frame.pack_forget() # Всё окно
        self.nav_frame.pack_forget() # Навигация
        self.preview_frame.pack_forget()
        self.save_btn.pack_forget() # Кнопка сохранения темы

    def start_new_theme(self): # Функция создания новой темы
        self.creating_theme = True # Ставим флаг на начало создания
        self.current_step = 0 # Первоначальный шаг
        self.theme_data = { # Берем каркас
            "name": "",
            "bg_color": "",
            "text_color": "",
            "selection_bg": "",
            "tags": {
                "system": "",
                "error": "",
                "success": "",
                "info": "",
                "command": "",
                "output": ""
            }
        }
    
        self.main_text.pack_forget() # Меняем текст в зависимости от шага
        self.update_step() # Переходим на следующий шаг

    def update_step(self): # Функция изменения шага
        self.step_label.config(text=self.steps[self.current_step])
        self.step_label.pack() # Текст который меняется при шагах

        if self.current_step == 0: # Ввод названия
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.color_btn.pack_forget()
            self.entry_frame.pack()
        else: # Выбор цвета
            self.entry.config(state=tk.DISABLED)
            self.color_btn.pack(side=tk.LEFT, padx=5)
            self.entry_frame.pack()

        # Управление кнопками
        self.back_btn.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        
        # Не меняем кнопку в конце шагов
        self.next_btn.config(text="→", state=tk.NORMAL)
        self.nav_frame.pack(pady=10)

        # Показываем предпросмотр для цветов
        if self.current_step > 0:
            try: # Отлавливаем ошибку (которая появляется из недр Tkinter)
                self.show_preview()
            except Exception:
                pass
        else:
            self.preview_frame.pack_forget()
            self.save_btn.pack_forget()

    def choose_color(self): # Функция вызова палитры
        color = colorchooser.askcolor( # Выбранный цвет
            title=self.languages[self.current_lang]["color_btn"])[1]
        if color:
            self.entry.config(state=tk.NORMAL)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, color)
            self.entry.config(state=tk.DISABLED)

            # Сохраняем цвет в соответствующий параметр
            if self.current_step == 1:
                self.theme_data["bg_color"] = color # Цвет заднего фона терминала
            elif self.current_step == 2:
                self.theme_data["text_color"] = color # Цвет текста
            elif self.current_step == 3:
                self.theme_data["selection_bg"] = color # Цвет наведения. (Работает с интерфейсом программы)
            elif self.current_step == 4:
                self.theme_data["tags"]["system"] = color # Цвет системного текста
            elif self.current_step == 5:
                self.theme_data["tags"]["error"] = color # Цвет системной ошибки
            elif self.current_step == 6:
                self.theme_data["tags"]["success"] = color # Цвет успешно-выполненной операции
            elif self.current_step == 7:
                self.theme_data["tags"]["info"] = color # Цвет информации
            elif self.current_step == 8:
                self.theme_data["tags"]["command"] = color # Цвет комманды
            elif self.current_step == 9:
                self.theme_data["tags"]["output"] = color # Цвет вывода 
            
            try: # Отлавливаем ошибку (которая появляется из недр Tkinter)
                self.show_preview()
            except Exception:
                pass

    def show_preview(self): # Функция предпросмотра для удобства
        # Показывает предпросмотр текущих цветов
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        self.preview_labels = [] # В самом начале, список пуст

        if self.current_step >= 1 and self.theme_data["bg_color"]: # По мере изменения, будет заполняется
            # автоматически, приблизительно показывая как будет выглядить тема
            lbl = tk.Label(
                self.preview_frame,
                text="Пример фона" if self.current_lang == "Русский" else "Background example",
                bg=self.theme_data["bg_color"],
                fg="white" if self.current_step < 2 else self.theme_data["text_color"],
                padx=20,
                pady=10
            )
            lbl.pack(pady=5, fill=tk.X, padx=50)
            self.preview_labels.append(lbl)

        if self.current_step >= 4: 
            tags = {
                "system": "Пример системного текста" if self.current_lang == "Русский" else "System text example",
                "error": "Пример ошибки" if self.current_lang == "Русский" else "Error example",
                "success": "Пример успеха" if self.current_lang == "Русский" else "Success example",
                "info": "Пример информации" if self.current_lang == "Русский" else "Info example",
                "command": "Пример команды" if self.current_lang == "Русский" else "Command example",
                "output": "Пример вывода" if self.current_lang == "Русский" else "Output example"
            }

            for tag, text in tags.items():
                if self.current_step >= 4 + list(self.theme_data["tags"].keys()).index(tag):
                    if self.theme_data["tags"][tag]:
                        lbl = tk.Label(
                            self.preview_frame,
                            text=text,
                            bg=self.theme_data["bg_color"] if self.theme_data["bg_color"] else "white",
                            fg=self.theme_data["tags"][tag],
                            padx=20,
                            pady=5
                        )
                        lbl.pack(pady=2, fill=tk.X, padx=30)
                        self.preview_labels.append(lbl)

        self.preview_frame.pack(expand=True, fill=tk.BOTH, pady=10)

    def next_step(self): # Функция перехода на следующий шаг
        # Переход к следующему шагу
        if self.current_step == 0:  # Проверяем название темы
            name = self.entry.get().strip()
            if not name:
                messagebox.showerror(
                    self.languages[self.current_lang]["error_title"],
                    self.languages[self.current_lang]["name_error"]
                )
                return
            self.theme_data["name"] = name
        elif self.current_step in [1, 2, 3, 4, 5, 6, 7, 8, 9]:  # Проверяем цвет
            if not self.entry.get().strip():
                messagebox.showerror(
                    self.languages[self.current_lang]["error_title"],
                    self.languages[self.current_lang]["color_error"]
                )
                return

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            try: # Отлавливаем ошибку (которая появляется из недр Tkinter)
                self.update_step()
            except Exception:
                pass
        else:
            # Проверяем, что все цвета заданы
            if not all(self.theme_data["tags"].values()):
                messagebox.showerror( # Если пользователь ничего не ввёл, показываем ошибку
                    self.languages[self.current_lang]["error_title"], 
                    self.languages[self.current_lang]["all_colors_error"]
                )
                return

            # Все шаги завершены, показываем кнопку сохранения
            self.save_btn.pack(pady=10)
            self.next_btn.config(state=tk.DISABLED)
            self.save_btn.config(state=tk.NORMAL)

    def prev_step(self): # Функция возврата к предыдущему шагу
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step()
            self.save_btn.pack_forget()
            self.next_btn.config(state=tk.NORMAL)

    def save_theme(self): # Функция Сохранения тем в JSON файл
        # Проверяем, что все поля заполнены
        required_fields = [
            self.theme_data["name"],
            self.theme_data["bg_color"],
            self.theme_data["text_color"],
            self.theme_data["selection_bg"],
            self.theme_data["tags"].values()
        ]

        if not all(required_fields):
            messagebox.showerror(
                self.languages[self.current_lang]["error_title"], # Если некоторые поля не были заполнены
                self.languages[self.current_lang]["fields_error"] # Показываем ошибочку
            )
            return

        # Добавляем фиксированные значения для cmd
        full_theme = {
            "name": self.theme_data["name"],
            "bg_color": self.theme_data["bg_color"],
            "text_color": self.theme_data["text_color"],
            "menu_bg": "#1E1E3F",
            "menu_fg": "#FFFFFF",
            "cmd_bg": "#0A0A1E",
            "cmd_fg": "#E0E0FF",
            "selection_bg": self.theme_data["selection_bg"],
            "tags": self.theme_data["tags"]
        }

        # Предлагаем выбрать место для сохранения
        file_path = filedialog.asksaveasfilename( # СОХРАНЯТЬ СТОИТ В КОРНЕВОЙ ПАПКЕ
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"{self.theme_data['name'].lower().replace(' ', '_')}_theme.json"
        )

        if file_path: # Проверяем все ошибки и нуансы
            try:
                with open(file_path, 'w') as f:
                    json.dump({self.theme_data['name'].lower().replace(
                        ' ', '_'): full_theme}, f, indent=4)

                messagebox.showinfo(
                    self.languages[self.current_lang]["success_title"],
                    self.languages[self.current_lang]["success_msg"].format(
                        self.theme_data['name'])
                )

                # Возвращаемся на начальный экран
                self.show_initial_screen()

            except Exception as e:
                messagebox.showerror(
                    self.languages[self.current_lang]["error_title"],
                    self.languages[self.current_lang]["save_error"].format(
                        str(e))
                )
if __name__ == "__main__": # Точка входа
    root = tk.Tk()
    try: # Пытаемся получить доступ к путю иконки
        script_dir = os.path.dirname(os.path.abspath(__file__)) # Обозначаем полный путь к проекту
        icon_path = os.path.join(script_dir, "dostt.ico") # Задаем путь
        
        if os.path.exists(icon_path): # Если программа нашла путь:
            root.iconbitmap(icon_path) # Применяем иконку
        else: # Если нет, то пропускаем всё
            pass
    except Exception as e:
        pass # Да, я тоже удивлен почему одна иконка занимает так много места в коде
    app = ThemeCreator(root) # Инициализируем приложение
    root.mainloop()