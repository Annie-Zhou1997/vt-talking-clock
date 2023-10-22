import sys
import os
import pytz
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox
from gtts import gTTS
from playsound import playsound
from datetime import datetime

class TalkingClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.timezone = pytz.timezone('UTC')
        self.format_24hr = False
        self.init_ui()
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)
        self.show_time()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { font-size: 20px; }")
        layout.addWidget(self.label)
        self.play_button = QPushButton('English', self)
        self.play_button.clicked.connect(self.play_time_en)
        layout.addWidget(self.play_button)
        self.play_button_zh = QPushButton('中文', self)
        self.play_button_zh.clicked.connect(self.play_time_zh)
        layout.addWidget(self.play_button_zh)
        self.play_button_ru = QPushButton('Русский', self)
        self.play_button_ru.clicked.connect(self.play_time_ru)
        layout.addWidget(self.play_button_ru)
        self.play_button_nl = QPushButton('Nederlands', self)
        self.play_button_nl.clicked.connect(self.play_time_nl)
        layout.addWidget(self.play_button_nl)
        self.timezone_combo = QComboBox(self)
        self.timezone_combo.addItems(pytz.all_timezones)
        self.timezone_combo.currentIndexChanged.connect(self.update_timezone)
        layout.addWidget(self.timezone_combo)
        self.format_checkbox = QCheckBox('24 Hour Format', self)
        self.format_checkbox.stateChanged.connect(self.update_format)
        layout.addWidget(self.format_checkbox)
        self.setLayout(layout)
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Talking Clock')

    def show_time(self):
        current_time = datetime.now(self.timezone)
        time_format = '%I:%M:%S %p' if not self.format_24hr else '%H:%M:%S'
        time_text = current_time.strftime(time_format)
        self.label.setText(time_text)

    def play_time(self, lang='en'):
        current_time = datetime.now(self.timezone)
        time_text = current_time.strftime('%I:%M %p' if not self.format_24hr else '%H:%M')
        if lang == 'zh':
            prefix = "现在时间是"
        elif lang == 'ru':
            prefix = "Текущее время"
        elif lang == 'nl':
            prefix = "De huidige tijd is"
        else:
            prefix = "The current time is"
        text_to_speak = f"{prefix} {time_text}"
        tts = gTTS(text=text_to_speak, lang=lang)
        tts.save("time.mp3")
        playsound("time.mp3")
        os.remove("time.mp3")

    def play_time_en(self):
        self.play_time('en')

    def play_time_zh(self):
        self.play_time('zh')

    def play_time_ru(self):
        self.play_time('ru')

    def play_time_nl(self):
        self.play_time('nl')

    def update_timezone(self):
        selected_timezone = self.timezone_combo.currentText()
        self.timezone = pytz.timezone(selected_timezone)

    def update_format(self):
        self.format_24hr = self.format_checkbox.isChecked()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TalkingClockApp()
    ex.show()
    sys.exit(app.exec())
