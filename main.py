import sys
import os
import pytz
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox, QComboBox, QStylePainter, QStyle, QStyleOptionComboBox, QGridLayout
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtGui import QRadialGradient
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
        layout = QGridLayout(self)

        # 在这里创建 ClockWidget 的实例并将其添加到布局中
        self.clock_widget = ClockWidget(self)
        layout.addWidget(self.clock_widget, 0, 0, 1, 3)
        # 设置窗口标题和大小
        self.setWindowTitle('Talking Clock')
        self.setGeometry(100, 100, 600, 600)

        # 电子时钟标签
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { font-size: 40px; }")
        self.label.setGeometry(150, 345, 300, 50)  # 设置电子时钟的位置和大小

        # English button
        self.play_button = QPushButton('English', self)
        self.play_button.setGeometry(250, 400, 100, 30)  # 设置按钮的位置和大小
        self.play_button.clicked.connect(self.play_time_en)

        # Chinese button
        self.play_button_zh = QPushButton('中文', self)
        self.play_button_zh.setGeometry(250, 450, 100, 30)  # 设置按钮的位置和大小
        self.play_button_zh.clicked.connect(self.play_time_zh)

        # Russian button
        self.play_button_ru = QPushButton('Русский', self)
        self.play_button_ru.setGeometry(250, 500, 100, 30)  # 设置按钮的位置和大小
        self.play_button_ru.clicked.connect(self.play_time_ru)

        # Dutch button
        self.play_button_nl = QPushButton('Nederlands', self)
        self.play_button_nl.setGeometry(250, 550, 100, 30)  # 设置按钮的位置和大小
        self.play_button_nl.clicked.connect(self.play_time_nl)

        # Timezone combo box
        self.timezone_combo = CustomComboBox(self)
        self.timezone_combo.addItem("Select Other Timezone")
        for tz in pytz.all_timezones:
            self.timezone_combo.addItem(tz)
        self.timezone_combo.setGeometry(10, 10, 190, 30)  # 设置组合框的位置和大小
        self.timezone_combo.currentIndexChanged.connect(self.update_timezone)

        # 24 hour format checkbox
        self.format_checkbox = QCheckBox('24 Hour Format', self)
        self.format_checkbox.setGeometry(20, 560, 200, 30)  # 设置复选框的位置和大小
        self.format_checkbox.stateChanged.connect(self.update_format)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #fbc2eb, stop:1 #a6c1ee);
            }
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 10px;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #dadbde, stop: 1 #f6f7fa);
            }
            QLabel, QComboBox, QCheckBox {
                background: transparent;
                border: none;
            }
            QLabel {
                font-family: 'PixelArmy';
                font-size: 40px;
            }
            QComboBox QAbstractItemView {
                background-color: #e2ebf0;
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
        if selected_timezone == 'Select Other Timezone':
            self.timezone = tz.tzlocal()
        else:
            self.timezone = pytz.timezone(selected_timezone)

    def update_format(self):
        self.format_24hr = self.format_checkbox.isChecked()

    def update_timezone(self):
        selected_timezone = self.timezone_combo.currentText()
        if selected_timezone == 'Select Other Timezone':
            self.timezone = tz.tzlocal()
        else:
            self.timezone = pytz.timezone(selected_timezone)
        self.clock_widget.set_timezone(self.timezone)  # 更新钟表表盘的时区

class ClockWidget(QWidget):
    def __init__(self, parent=None):
        super(ClockWidget, self).__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        self.timezone = tz.tzlocal()  # 默认使用本地时区

    def set_timezone(self, timezone):
        self.timezone = timezone
        self.update()  # 立即更新钟表表盘

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        self.draw_clock(painter)
        painter.end()

    def draw_clock(self, painter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center_x = self.width() / 2
        center_y = self.height() / 3.5
        clock_radius = min(self.width(), self.height()) / 4
        painter.translate(center_x, center_y)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 绘制表盘
        gradient = QRadialGradient(0, 0, clock_radius)
        gradient.setColorAt(0, QColor(226, 235, 240))
        gradient.setColorAt(1, QColor(207, 217, 233))
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(int(-clock_radius), int(-clock_radius), int(2 * clock_radius), int(2 * clock_radius))

        # 绘制刻度
        for i in range(12):
            painter.drawLine(0, round(-clock_radius), 0, round(-clock_radius + 10))
            painter.rotate(30)

        # 获取当前时间
        current_time = datetime.now(self.timezone).time()
        secs = current_time.second
        mins = current_time.minute + secs / 60
        hrs = current_time.hour + mins / 60

        # 绘制时针
        painter.setPen(QPen(QColor(50, 50, 50), 6))
        painter.setBrush(QColor(50, 50, 50))
        painter.rotate(hrs * (360 / 12))
        painter.drawRect(-5, int (-clock_radius / 2), 10, int(clock_radius / 2))  # 使用矩形作为时针
        painter.rotate(-hrs * (360 / 12))

        # 绘制分针
        painter.setPen(QPen(QColor(0, 0, 0), 4))
        painter.rotate(mins * (360 / 60))
        painter.drawLine(0, 0, 0, round(-clock_radius * 0.7))
        painter.rotate(-mins * (360 / 60))

        # 绘制秒针
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.rotate(secs * (360 / 60))
        painter.drawLine(0, 0, 0, round(-clock_radius * 0.9))
        painter.rotate(-secs * (360 / 60))

        painter.restore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TalkingClockApp()
    ex.show()
    ex.setGeometry(100, 100, 600, 600)
    sys.exit(app.exec())
