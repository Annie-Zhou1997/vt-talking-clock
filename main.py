import sys
import os
import pytz
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox, QComboBox, QStylePainter, QStyle, QStyleOptionComboBox
from gtts import gTTS
from playsound import playsound
from datetime import datetime
from dateutil import tz
import time

class CustomComboBox(QComboBox):
    def paintEvent(self, event):
        painter = QStylePainter(self)
        painter.setPen(self.palette().color(self.foregroundRole()))

        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)

        painter.drawComplexControl(QStyle.ComplexControl.CC_ComboBox, opt)
        painter.drawControl(QStyle.ControlElement.CE_ComboBoxLabel, opt)

class TalkingClockApp(QWidget):

    def __init__(self):
        super().__init__()
        local_timezone = time.tzname[0]
        self.timezone = pytz.timezone(local_timezone)
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
        self.label.setStyleSheet("QLabel { font-size: 40px; }")
        layout.addWidget(self.label)

        # English button
        h_layout_en = QHBoxLayout()
        self.play_button = QPushButton('English', self)
        self.play_button.setMinimumWidth(95)  # 设置最大宽度
        self.play_button.clicked.connect(self.play_time_en)
        h_layout_en.addStretch()
        h_layout_en.addWidget(self.play_button)
        h_layout_en.addStretch()
        layout.addLayout(h_layout_en)

        # Chinese button
        h_layout_zh = QHBoxLayout()
        self.play_button_zh = QPushButton('中文', self)
        self.play_button_zh.setMinimumWidth(95)  # 设置最大宽度
        self.play_button_zh.clicked.connect(self.play_time_zh)
        h_layout_zh.addStretch()
        h_layout_zh.addWidget(self.play_button_zh)
        h_layout_zh.addStretch()
        layout.addLayout(h_layout_zh)

        # Russian button
        h_layout_ru = QHBoxLayout()
        self.play_button_ru = QPushButton('Русский', self)
        self.play_button_ru.setMinimumWidth(95)  # 设置最大宽度
        self.play_button_ru.clicked.connect(self.play_time_ru)
        h_layout_ru.addStretch()
        h_layout_ru.addWidget(self.play_button_ru)
        h_layout_ru.addStretch()
        layout.addLayout(h_layout_ru)

        # Dutch button
        h_layout_nl = QHBoxLayout()
        self.play_button_nl = QPushButton('Nederlands', self)
        self.play_button_nl.setMinimumWidth(95)  # 设置最大宽度
        self.play_button_nl.clicked.connect(self.play_time_nl)
        h_layout_nl.addStretch()
        h_layout_nl.addWidget(self.play_button_nl)
        h_layout_nl.addStretch()
        layout.addLayout(h_layout_nl)

        # Timezone combo box
        self.timezone_combo = CustomComboBox(self)
        self.timezone_combo.addItem("Select Other Timezone")  # default
        for tz in pytz.all_timezones:
            self.timezone_combo.addItem(tz)
        self.timezone_combo.currentIndexChanged.connect(self.update_timezone)
        layout.addWidget(self.timezone_combo)

        # 24 hour format checkbox
        self.format_checkbox = QCheckBox('24 Hour Format', self)
        self.format_checkbox.stateChanged.connect(self.update_format)
        layout.addWidget(self.format_checkbox)
        self.setLayout(layout)
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Talking Clock')
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #fbc2eb, stop:1 #a6c1ee);  /* 主背景渐变色 Основной фон градиентного цвета*/
            }
            QPushButton {
                border: 2px solid #8f8f91;  /* 按钮边框颜色 Цвет границы кнопки */
                border-radius: 10px;  /* 按钮圆角大小 Размер закругления кнопки */
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);  /* 按钮背景渐变色 Цвет фонового градиента кнопки */
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #dadbde, stop: 1 #f6f7fa);  /* 按钮被按下时的背景渐变色 */
            }
            QLabel, QComboBox, QCheckBox {
                background: transparent;  /* 标签、组合框和复选框背景透明 */
                border: none;  /* 无边框 */
            }
            QLabel {
                font-family: 'PixelArmy';  /* 电子时钟字体 */
                font-size: 40px;  /* 字体大小 */
            }
            QComboBox QAbstractItemView {
                background-color: #e2ebf0;  /* 设置下拉菜单打开后的项的背景颜色 */
            }
        """)


    def show_time(self):
        selected_timezone = self.timezone_combo.currentText()
        if selected_timezone == 'Select Other Timezone':
            current_time = datetime.now(tz.tzlocal())
        else:
            timezone = pytz.timezone(selected_timezone)
            current_time = datetime.now(timezone)
        time_format = '%I:%M:%S %p' if not self.format_24hr else '%H:%M:%S'
        time_text = current_time.strftime(time_format)
        self.label.setText(time_text)

    def play_time(self, lang='en'):
        selected_timezone = self.timezone_combo.currentText()
        if selected_timezone == 'Select Other Timezone':
            current_time = datetime.now(tz.tzlocal())
        else:
            timezone = pytz.timezone(selected_timezone)
            current_time = datetime.now(timezone)
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
