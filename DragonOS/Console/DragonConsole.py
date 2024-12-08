import re
import sys
import threading
from comm import *
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

def comm(commands):
    if commands=='': return None
    cmd=commands.split('\n')
    for command in cmd:
        print("[38;5;10mfor[38;5;220m<<"+str(command))
        args=command.split(" ")
        func=args[0]
        del args[0]
        eval(func+"(*"+str(args)+")")
def run(path):
    path='home/'+path
    file = open(path).read()
    for cmd in file.split('\n'):
        eval(path.split('.')[-1]+'("'+cmd+'")')
def connect(link):
    connectLib.append(link)
def reload():
    for f in os.listdir("adding/comm/"):
        name=f.split(".")[0]
        print("[38;5;11madding.comm."+name+"...",end='')
        try:
            globals()[name]=importlib.import_module("adding.comm."+name)
            print('[38;5;10mLOAD')
        except:
            print('[38;5;1mERROR')
    for f in connectLib:
        print("[38;5;11m"+f+"...",end='')
        try:
            globals()[f.split('/')[-1]]=importlib.import_module(f)
            print('[38;5;10mLOAD')
        except:
            print('[38;5;1mERROR')
    for f in os.listdir("home/auto/"):
        print('runing:'+f)
        run('auto/'+f)
        
def remove_color_codes(text):
    # Используем регулярное выражение для удаления нужных кодов
    cleaned_text = re.sub(r'\[\d{1,2};5;\d{1,3}m', '', text)
    return cleaned_text

# Функция преобразования ANSI-кода в RGB
def ansi_to_rgb(code):
    match = re.search(r'\[38;5;(\d+)', code)
    if match:
        code = int(match.group(1))
    else:
        raise ValueError("Неверный формат ANSI-кода.")
    if 0 <= code <= 7:
        base_colors = [
            (0, 0, 0),
            (128, 0, 0),
            (0, 128, 0),
            (128, 128, 0),
            (0, 0, 128),
            (128, 0, 128),
            (0, 128, 128),
            (192, 192, 192)
        ]
        return base_colors[code]
    elif 8 <= code <= 15:
        bright_colors = [
            (128, 128, 128),
            (255, 0, 0),
            (0, 255, 0),
            (255, 255, 0),
            (0, 0, 255),
            (255, 0, 255),
            (0, 255, 255),
            (255, 255, 255)
        ]
        return bright_colors[code - 8]
    elif 16 <= code <= 231:
        code -= 16
        r = (code // 36) * 51
        g = ((code // 6) % 6) * 51
        b = (code % 6) * 51
        return (r, g, b)
    elif 232 <= code <= 255:
        gray = (code - 232) * 11 + 8
        return (gray, gray, gray)
    else:
        raise ValueError("ANSI-код должен быть в диапазоне 0–255.")


# Класс для перехвата стандартного вывода
class ConsoleOutput:
    def __init__(self, console_app):
        self.console_app = console_app

    def write(self, message):
        if message.strip():  # Игнорируем пустые строки
            self.console_app.add_ansi_output(remove_color_codes(message))

    def flush(self):
        pass  # Ничего не делаем для flush


class ConsoleApp(App):
    def build(self):
        # Основной макет
        layout = BoxLayout(orientation="vertical")

        # Поле ввода
        self.input_field = TextInput(
            size_hint=(1, None),
            height=50,
            multiline=False,
            hint_text="Введите команду и нажмите Enter"
        )
        self.input_field.bind(on_text_validate=self.execute_command)

        # Область вывода с прокруткой
        scroll_view = ScrollView(size_hint=(1, 1))
        self.console_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.console_layout.bind(minimum_height=self.console_layout.setter('height'))
        scroll_view.add_widget(self.console_layout)

        # Добавляем виджеты
        layout.add_widget(self.input_field)
        layout.add_widget(scroll_view)

        # Перенаправляем стандартный вывод
        sys.stdout = ConsoleOutput(self)

        return layout

    def execute_command(self, instance):
        """Обрабатываем команды и ловим исключения."""
        command = self.input_field.text.strip()
        if command:
            try:
                # Выполнение и вывод результатов
                comm(command)
            except Exception as e:
                # Если произошла ошибка, обрабатываем и показываем красным
                error_message = f"Ошибка: {e}"
                print(f"\x1b[38;5;196m{error_message}")
        self.input_field.text = ""

    def add_ansi_output(self, text):
        """Разбираем ANSI-коды и отображаем текст с цветами."""
        segments = self.parse_ansi(text)

        # Горизонтальный макет для этой строки
        row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)

        for segment_text, color in segments:
            label = Label(
                text=segment_text,
                size_hint_x=None,
                halign="left",
                valign="middle",
                text_size=(None, None),
                color=color
            )
            row_layout.add_widget(label)

        self.console_layout.add_widget(row_layout)

    def parse_ansi(self, text):
        """Парсим ANSI-коды и разбиваем текст на сегменты с цветами."""
        pattern = r'(\x1b\[38;5;(\d+)m.*?)(?=\x1b\[38;5;|$)'
        matches = re.finditer(pattern, text)
        segments = []
        last_end = 0

        for match in matches:
            # Добавляем текст до ANSI-кода как обычный цвет
            if match.start() > last_end:
                segments.append((text[last_end:match.start()], (1, 1, 1, 1)))

            # Получаем цвет
            ansi_code = int(match.group(2))
            rgb = ansi_to_rgb(f"\x1b[38;5;{ansi_code}m")
            segments.append((match.group(1), (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, 1)))
            last_end = match.end()

        # Добавляем оставшийся текст
        if last_end < len(text):
            segments.append((text[last_end:], (1, 1, 1, 1)))

        return segments