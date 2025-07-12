import tkinter as tk
from tkinter import scrolledtext, Entry, Frame, Label, Menu
import subprocess
import os
import json
import sys


class DOSEmulator:  # Основной класс нашей оболочки
    CONFIG_FILE = "dos_em_config.json"  # Файл конфигурации

    THEMES = {  # ТЕМЫ!
        "standard": {
            "name": "Standard",
            "bg_color": '#000000',
            "text_color": '#C0C0C0',
            "menu_bg": '#C0C0C0',
            "menu_fg": 'white',
            "cmd_bg": 'black',
            "cmd_fg": 'white',
            "selection_bg": "#565656",
            "tags": {
                "system": '#C0C0C0',
                "error": '#C0C0C0',
                "success": '#C0C0C0',
                "info": '#C0C0C0',
                "command": '#C0C0C0',
                "output": '#C0C0C0'
            }
        },
        "msdosblue": {
            "name": "MS-DOS Blue",
            "bg_color": '#0200a9',
            "text_color": '#C0C0C0',
            "menu_bg": '#C0C0C0',
            "menu_fg": 'black',
            "cmd_bg": 'white',
            "cmd_fg": 'black',
            "selection_bg": "#2626FF",
            "tags": {
                "system": '#C0C0C0',
                "error": '#C0C0C0',
                "success": '#C0C0C0',
                "info": '#AAAAAA',
                "command": '#C0C0C0',
                "output": "#050404"
            }
        },
        "ubuntu": {
            "name": "Ubuntu",
            "bg_color": '#300924',
            "text_color": '#9ee369',
            "menu_bg": '#C0C0C0',
            "menu_fg": 'black',
            "cmd_bg": 'white',
            "cmd_fg": 'black',
            "selection_bg": "#95407B",
            "tags": {
                "system": '#9ee369',
                "error": '#EF2929',
                "success": '#8AE234',
                "info": '#888A85',
                "command": '#FCE94F',
                "output": '#9ee369'
            }
        },
        # "пример": { Можете заменить этот JSON на любой созданный вами в программе dosem_theme_creator!
        #         "name": "Пример",
        #         "bg_color": "#5458ed",
        #         "text_color": "#fffb42",
        #         "menu_bg": "#1E1E3F",
        #         "menu_fg": "#FFFFFF",
        #         "cmd_bg": "#0A0A1E",
        #         "cmd_fg": "#E0E0FF",
        #         "selection_bg": "#6f6cd5",
        #         "tags": {
        #             "system": "#a0a0a0",
        #             "error": "#abbe83",
        #             "success": "#44cafd",
        #             "info": "#f8cc49",
        #             "command": "#46fbe4",
        #             "output": "#d96868"
        #     }
        # }
    }

    # НИЖЕ ИДЕТ ФУНКЦИОНАЛ ПРОГРАММЫ. ЕСЛИ ВЫ НЕОПЫТНЫЙ ПОЛЬЗОВАТЕЛЬ, ПОЖАЛУЙСТА, НЕ ИЗМЕНЯЙТЕ КОД.
    # В ЛЮБОМ СЛУЧАЕ, МОДИФИЦИРОВАННЫЕ ВЕРСИИ МОЕГО ПРИЛОЖЕНИЯ ТАКЖЕ ПРИВЕТСТВУЮТСЯ, ЕСЛИ ВЫ СУМЕЕТЕ РАЗОБРАТЬСЯ В КОДЕ.
    # BELOW IS THE FUNCTIONALITY OF THE PROGRAM. IF YOU ARE A NON PROFESSIONAL USER, PLEASE DO NOT REDACT THE CODE.
    # IN ANY CASE, MODIFIED VERSIONS OF MY APPLICATION ARE ALSO WELCOME IF YOU CAN FIGURE OUT THE CODE.

    def __init__(self, root):  # Конструктор полей для тем (НЕ ТРОГАТЬ)
        self.current_theme = self.config.get("theme", "standard")
        self.apply_theme()

    def __init__(self, root):  # Конструктор полей
        self.root = root
        self.root.title("DOSem v1.4")  # Название окна
        self.root.geometry("640x480")  # Первоначальный размер
        self.root.minsize(640, 480)  # Минимальный размер

        # Загружаем конфигурацию
        # Загружаем конфигурацию (если пользователь открывал программу)
        self.config = self.load_config()

        # Настройки языка
        # Настроойки языка по умолчанию
        self.language = self.config.get("language", "ru")  # Конфиг локализации
        self.localization = {
            "en": {
                "file": "File",
                "exit": "Exit",
                "themes": "Themes",
                "options": "Options",
                "language": "Language",
                "english": "English",
                "russian": "Russian"
            },
            "ru": {
                "file": "Файл",
                "exit": "Выход",
                "themes": "Темы",
                "options": "Настройки",
                "language": "Язык",
                "english": "Английский",
                "russian": "Русский"
            }
        }

        # Текущая тема (загружаемая из конфига или по умолчанию)
        self.current_theme = self.config.get("theme", "standard")
        self.apply_theme()
        self.load_custom_themes()

        # История команд
        self.command_history = []  # Пустой список
        self.history_index = -1

        # Текущий каталог
        self.current_dir = os.getcwd()

        # Создание интерфейса
        self.create_widgets()  # 'Маунтим на основное окно виджеты
        self.create_menu()  # Создаем меню
        self.update_prompt()

        # Cообщение при старте
        # self.append_text - отвечает за вывод сообщений в терминал
        self.append_text(
            "CD-ROM-SOFT\nDOSem\nVersion 1.4\n(C) Copyright 2025 Python Corp\n\n", 'system')
        self.append_text(
            f"Current directory is {self.current_dir}\n\n", 'info')
        self.append_text("Type 'help' for available commands\n\n", 'command')

        # Сохраняем конфигурацию при закрытии
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_config(self):  # Функция загрузки настроек
        # Загружает конфигурацию из файла
        default_config = {
            "theme": "standard",
            "language": "en"
        }

        try:  # Пытаемся загрузить настройки из файла-конфигуратора
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:  # Отлов ошибки
            pass

        return default_config

    def save_config(self):  # Функция сохрранения пользовательских настроек
        # Сохраняет текущую конфигурацию в файл
        config = {
            "theme": self.current_theme,
            "language": self.language
        }
        try:  # Пытаемся открыть json конфиг
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            pass

    def on_close(self):  # Функция закрытия
        # Обработчик закрытия окна
        self.save_config()  # Перед тем как закроется программа, сохраняем настройки пользователя
        self.root.destroy()  # А потом закрываем окно

    def load_custom_themes(self):  # НЕ ТРОГАТЬ. DO NOT TOUCH
        CUSTOM_THEMES_FILE = "custom_themes.json"
        try:
            if os.path.exists(CUSTOM_THEMES_FILE):
                with open(CUSTOM_THEMES_FILE, 'r') as f:
                    custom_themes = json.load(f)

                    for theme_id, theme_data in custom_themes.items():
                        if theme_id not in self.THEMES:  # Не перезаписываем стандартные темы
                            self.THEMES[theme_id] = theme_data
        except Exception as e:
            pass

    def save_custom_theme(self, theme_id, theme_data):  # DO NOT TOUCH. НЕ ТРОГАТЬ
        CUSTOM_THEMES_FILE = "custom_themes.json"

        try:
            existing_themes = {}
            if os.path.exists(CUSTOM_THEMES_FILE):
                with open(CUSTOM_THEMES_FILE, 'r') as f:
                    existing_themes = json.load(f)

            existing_themes[theme_id] = theme_data

            with open(CUSTOM_THEMES_FILE, 'w') as f:
                json.dump(existing_themes, f, indent=4)

            return True
        except Exception as e:
            pass
            return False

    def apply_theme(self):  # Функция применения темы
        # конфиг при первом запуске
        theme = self.THEMES.get(self.current_theme, self.THEMES["standard"])

        # Основные цвета
        self.bg_color = theme["bg_color"]  # Все значения берем из JSON THEME
        # Все значения берем из JSON THEME
        self.text_color = theme["text_color"]
        self.menu_bg = theme["menu_bg"]  # Все значения берем из JSON THEME
        self.menu_fg = theme["menu_fg"]  # Все значения берем из JSON THEME
        self.cmd_bg = theme["cmd_bg"]  # Все значения берем из JSON THEME
        self.cmd_fg = theme["cmd_fg"]  # Все значения берем из JSON THEME
        # Все значения берем из JSON THEME
        self.selection_bg = theme["selection_bg"]

        # Обновляем цвета тегов, если виджеты уже созданы
        if hasattr(self, 'output'):  # Также кастомные цвета для системного текста
            tags_config = {
                'system': {'foreground': theme["tags"]["system"]},
                'error': {'foreground': theme["tags"]["error"]},
                'success': {'foreground': theme["tags"]["success"]},
                'info': {'foreground': theme["tags"]["info"]},
                'command': {'foreground': theme["tags"]["command"]},
                'output': {'foreground': theme["tags"]["output"]}
            }

            for tag, config in tags_config.items():
                self.output.tag_config(tag, **config)

    def create_menu(self):  # Функция создания меню
        # Создаёт меню в верхней части окна
        menubar = Menu(self.root)  # Панелька меню

        # Меню File
        file_menu = Menu(menubar, tearoff=0, bg=self.menu_bg, fg=self.menu_fg,
                         activebackground=self.selection_bg, activeforeground=self.menu_fg)  # Маунтим панельку
        # Под пункт для File
        file_menu.add_command(
            label=self.localization[self.language]["exit"], command=self.on_close)
        menubar.add_cascade(
            # Сама кнопка
            label=self.localization[self.language]["file"], menu=file_menu)

        # Меню Themes
        themes_menu = Menu(menubar, tearoff=0, bg=self.menu_bg, fg=self.menu_fg,
                           activebackground=self.selection_bg, activeforeground=self.menu_fg)

        # Динамически добавляем темы из коллекции THEMES
        for theme_id, theme_data in self.THEMES.items():
            themes_menu.add_command(
                label=theme_data["name"],
                command=lambda tid=theme_id: self.change_theme(tid)
            )

        menubar.add_cascade(
            label=self.localization[self.language]["themes"], menu=themes_menu)

        # Меню Options
        options_menu = Menu(menubar, tearoff=0, bg=self.menu_bg, fg=self.menu_fg,
                            activebackground=self.selection_bg, activeforeground=self.menu_fg)

        # Подменю Language
        language_menu = Menu(options_menu, tearoff=0, bg=self.menu_bg, fg=self.menu_fg,
                             activebackground=self.selection_bg, activeforeground=self.menu_fg)
        language_menu.add_command(label=self.localization[self.language]["english"],
                                  command=lambda: self.change_language("en"))
        language_menu.add_command(label=self.localization[self.language]["russian"],
                                  command=lambda: self.change_language("ru"))

        options_menu.add_cascade(
            label=self.localization[self.language]["language"], menu=language_menu)
        menubar.add_cascade(
            label=self.localization[self.language]["options"], menu=options_menu)

        self.root.config(menu=menubar)

    def change_language(self, lang): # Функция смены языка
        # Меняет язык интерфейса
        self.language = lang
        self.create_menu()  # Пересоздаем меню с новым языком
        self.append_text(f"Language changed to {lang}\n", 'system')
        self.save_config()

    def change_theme(self, theme_name):  # Функция смены темы
        self.current_theme = theme_name  # Применяем тему
        self.save_config()  # Сохраняем конфигурацию
        # Обязательно перезапускаем программу, что бы пользователь не видел мешанину при смене темы
        # Закрываем текущее окно
        self.root.destroy()

        # Перезапускаем приложение
        self.restart_program()

    def restart_program(self):  # Функция перезапуска
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def create_widgets(self):  # Функция маутинга виджетов
        self.output = scrolledtext.ScrolledText(
            self.root, bg=self.bg_color, fg=self.text_color,
            font=('More Perfect DOS VGA', 12), insertbackground=self.text_color, # Настолятельно рекомендую установить шрифт.
            wrap=tk.WORD, state='disabled'
        )
        self.output.pack(expand=True, fill='both', padx=5, pady=5)

        # Настройка тегов для цветного текста с использованием цветов из темы
        theme = self.THEMES.get(self.current_theme, self.THEMES["standard"])
        self.output.tag_config('system', foreground=theme["tags"]["system"])
        self.output.tag_config('error', foreground=theme["tags"]["error"])
        self.output.tag_config('success', foreground=theme["tags"]["success"])
        self.output.tag_config('info', foreground=theme["tags"]["info"])
        self.output.tag_config('command', foreground=theme["tags"]["command"])
        self.output.tag_config('output', foreground=theme["tags"]["output"])

        # Панель ввода команд, input
        self.cmd_frame = Frame(self.root, bg=self.cmd_bg)
        self.cmd_frame.pack(fill='x', padx=5, pady=(0, 5))

        self.prompt = Label(self.cmd_frame, text="C:\\>",
                            bg=self.cmd_bg, fg=self.cmd_fg, font=('Consolas', 12))
        self.prompt.pack(side='left')

        self.cmd_entry = Entry(self.cmd_frame, bg=self.cmd_bg, fg=self.cmd_fg,
                               insertbackground=self.cmd_fg, font=(
                                   'Consolas', 12),
                               relief='flat')
        self.cmd_entry.pack(side='left', fill='x', expand=True)
        self.cmd_entry.bind('<Return>', self.execute_command)
        self.cmd_entry.bind('<Up>', self.prev_command)
        self.cmd_entry.bind('<Down>', self.next_command)
        self.cmd_entry.focus()

    def update_prompt(self):  # Функция-обработчик запроса
        drive = os.path.splitdrive(self.current_dir)[0] or 'C:'
        path = os.path.relpath(
            self.current_dir, os.path.splitdrive(self.current_dir)[0])
        prompt_text = f"{drive}{path}>"
        self.prompt.config(text=prompt_text)

    def execute_command(self, event):  # Функция-обработчик команд
        command = self.cmd_entry.get().strip()
        self.cmd_entry.delete(0, tk.END)

        if not command:
            return

        # Добавляем команду в историю
        self.command_history.append(command)
        self.history_index = -1

        # Выводим команду в текстовое поле
        self.append_text(
            f"\n{self.prompt.cget('text')} {command}\n", 'command')

        # Обработчик команд
        if command.lower() == 'exit':
            self.root.destroy()
            return
        elif command.lower() == 'help':
            self.show_help()
            return
        elif command.lower() == 'clear' or command.lower() == 'cls':
            self.output.configure(state='normal')
            self.output.delete(1.0, tk.END)
            self.output.configure(state='disabled')
            return
        elif command.lower().startswith('cd '):
            self.change_directory(command[3:].strip())
            return
        elif command.lower() == 'dir':
            self.show_dir_contents()
            return
        elif command.lower().startswith('read '):  # считыватель
            self.read_file(command[5:].strip())
            return
        elif command.lower() == 'ver':
            self.append_text("DOSem v1.4 (Python)\n", 'system')
            return
        elif command.lower() == 'python':  # Отлавливаем попытку открыть python в python
            self.append_text(
                "Sorry. You cannot run python in python program.", 'error')
            return

        # Выполнение системных команд
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.current_dir,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            if result.stdout:
                self.append_text(result.stdout + '\n', 'output')
            if result.stderr:
                self.append_text(result.stderr + '\n', 'error')
        except Exception as e:
            self.append_text(f"Error: {str(e)}\n", 'error')

    def change_directory(self, new_dir):  # Функция управления директориями
        # Обрабатывает команду смены каталога
        try:
            if not new_dir:
                self.append_text(
                    f"Current directory: {self.current_dir}\n", 'info')
                return

            if new_dir == '..':
                new_path = os.path.dirname(self.current_dir)
            elif new_dir == '/':
                new_path = os.path.splitdrive(self.current_dir)[0] or 'C:\\'
            else:
                new_path = os.path.abspath(
                    os.path.join(self.current_dir, new_dir))

            if os.path.isdir(new_path):
                os.chdir(new_path)
                self.current_dir = os.getcwd()
                self.update_prompt()
                self.append_text(
                    f"Directory changed to {self.current_dir}\n", 'success')
            else:
                self.append_text(f"Directory not found: {new_dir}\n", 'error')
        except Exception as e:
            self.append_text(f"Error: {str(e)}\n", 'error')

    def show_dir_contents(self):  # Функция считывания содержимого каталога
        # Показывает содержимое каталога
        try:
            contents = os.listdir(self.current_dir)
            dirs = [d for d in contents if os.path.isdir(
                os.path.join(self.current_dir, d))]
            files = [f for f in contents if not os.path.isdir(
                os.path.join(self.current_dir, f))]

            self.append_text(
                f"\n Directory of {self.current_dir}\n\n", 'system')

            for d in dirs:
                self.append_text(f"<DIR>\t{d}\n", 'info')

            for f in files:
                size = os.path.getsize(os.path.join(self.current_dir, f))
                self.append_text(f"\t{f}\t{size} bytes\n", 'output')

            self.append_text(
                f"\n\t{len(files)} file(s)\t{len(dirs)} dir(s)\n\n", 'info')
        except Exception as e:
            self.append_text(f"Error: {str(e)}\n", 'error')

    def read_file(self, filename):  # Функция считывания файла
        # Показывает содержимое файла
        try:
            filepath = os.path.join(self.current_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    self.append_text(
                        f"\nContents of {filename}:\n\n", 'system')
                    self.append_text(content + '\n', 'output')
            else:
                self.append_text(f"File not found: {filename}\n", 'error')
        except Exception as e:
            self.append_text(f"Error: {str(e)}\n", 'error')

    def show_help(self):  # Функция для вывода справки
        help_text = """
╔═[■]════════════ Help ══════════════╗
║Available commands:                 ║█
║help      - Show this help          ║█
║clear/cls - Clear the screen        ║█
║exit      - Exit the emulator       ║█
║cd <dir>  - Change directory        ║█
║dir       - List directory contents ║█
║read <file> - Show file contents    ║█
║ver       - Show version information║█
╚════════════════════════════════════╝█
 ██████████████████████████████████████
"""
        self.append_text(help_text, 'system')

    def prev_command(self, event):  # Функция предыдущей команды из истории
        if self.command_history:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(
                0, self.command_history[-(self.history_index+1)])

    def next_command(self, event):  # Функция следующей комманды из истории
        if self.history_index > 0:
            self.history_index -= 1
            self.cmd_entry.delete(0, tk.END)
            self.cmd_entry.insert(
                0, self.command_history[-(self.history_index+1)])
        elif self.history_index == 0:
            self.history_index = -1
            self.cmd_entry.delete(0, tk.END)

    # Функция вывода текста. Грубо говоря print()
    def append_text(self, text, tag='output'):
        self.output.configure(state='normal')
        self.output.insert(tk.END, text, tag)
        self.output.configure(state='disabled')
        self.output.see(tk.END)


if __name__ == "__main__":  # Точка входа
    root = tk.Tk()
    try:  # Устанавливаем самую лучшую иконку в мире
        root.iconbitmap(default='dos.ico')  # Задаем ей конкретное название
    except:  # Ну а если иконки нет
        pass  # То ничего не происходит

    emulator = DOSEmulator(root)
    root.mainloop()
