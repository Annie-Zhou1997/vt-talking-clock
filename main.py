import sys
import os
import pytz
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox, QComboBox, QStylePainter, QStyle, QStyleOptionComboBox, QGridLayout, QFileDialog
from PyQt6.QtWidgets import QTimeEdit
from PyQt6.QtWidgets import QCalendarWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtGui import QRadialGradient
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtCore import QPointF,QRectF, QDate
from gtts import gTTS
from playsound import playsound
from datetime import datetime
from dateutil import tz
import time
import math
from PyQt6.QtGui import QPixmap

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
        # 日期定时器 date timer
        self.date_timer = QTimer(self)
        self.date_timer.timeout.connect(self.update_date)
        self.date_timer.start(86400000)  # 每天更新一次 

        self.calendar_mini = QCalendarWidget(self)
        self.calendar_mini.setVisible(False)  # 初始时隐藏日历

    def init_ui(self):
        layout = QGridLayout(self)

        # 日期标签 date label
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("QLabel { font-size: 22px; }")
        self.date_label.setGeometry(180, 320, 250, 60)  # 你可以根据需要调整位置和大小
        self.update_date()

        # 在这里创建 ClockWidget 的实例并将其添加到布局中  create an instance of ClockWidget and add it to the layout
        self.clock_widget = ClockWidget(self)
        layout.addWidget(self.clock_widget, 0, 0, 1, 3)
        # 设置窗口标题和大小 set window title and size
        self.setWindowTitle('Talking Clock')
        self.setGeometry(100, 100, 600, 600)

        # 电子时钟标签 electronic clock label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { font-size: 40px; }")
        self.label.setGeometry(150, 380, 300, 50)  # 设置电子时钟的位置和大小 set position and size of electronic clock

        # English button
        self.play_button = QPushButton('English', self)
        self.play_button.setGeometry(250, 430, 100, 30)  # 设置按钮的位置和大小 set position and size of button
        self.play_button.clicked.connect(self.play_time_en)

        # Chinese button
        self.play_button_zh = QPushButton('中文', self)
        self.play_button_zh.setGeometry(250, 470, 100, 30)  # 设置按钮的位置和大小  set position and size of button
        self.play_button_zh.clicked.connect(self.play_time_zh)

        # Russian button
        self.play_button_ru = QPushButton('Русский', self)
        self.play_button_ru.setGeometry(250, 510, 100, 30)  # 设置按钮的位置和大小 set position and size of button
        self.play_button_ru.clicked.connect(self.play_time_ru)

        # Dutch button
        self.play_button_nl = QPushButton('Nederlands', self)
        self.play_button_nl.setGeometry(250, 550, 100, 30)  # 设置按钮的位置和大小 set position and size of button
        self.play_button_nl.clicked.connect(self.play_time_nl)

        # Timezone combo box
        self.timezone_combo = CustomComboBox(self)
        self.timezone_combo.addItem("Select Other Timezone")
        self.timezone_combo.addItem("UTC")
        self.timezone_combo.addItem("America/New_York")  
        self.timezone_combo.addItem("Europe/Amsterdam")  
        self.timezone_combo.addItem("Europe/London")
        self.timezone_combo.addItem("Asia/Shanghai")  # Beijing same as Shanghai
        self.timezone_combo.addItem("Europe/Moscow")
        self.timezone_combo.setGeometry(10, 10, 190, 30)
        self.timezone_combo.currentIndexChanged.connect(self.update_timezone)

        # 24 hour format checkbox
        self.format_checkbox = QCheckBox('24 Hour Format', self)
        self.format_checkbox.setGeometry(20, 560, 200, 30)  # 设置复选框的位置和大小  set position and size of checkbox
        self.format_checkbox.stateChanged.connect(self.update_format)

        # Set Alarm button
        self.alarm_button = QPushButton('Set Alarm', self)
        self.alarm_button.setGeometry(480, 10, 100, 30)  # 设置按钮的位置和大小 set position and size of button
        self.alarm_button.clicked.connect(self.show_alarm_window)
        
        # Full Calendar button
        self.toggle_calendar_button = QPushButton('Calendar', self)
        self.toggle_calendar_button.setGeometry(480, 50, 100, 30)
        self.toggle_calendar_button.clicked.connect(self.toggle_calendar)
        
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
    def open_full_calendar(self):
        self.calendar_window = CalendarWindow()
        self.calendar_window.show()

    def update_date(self):
        current_date = QDate.currentDate()
        self.date_label.setText(current_date.toString("yyyy-MM-dd dddd"))

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
        self.clock_widget.set_timezone(self.timezone)  # 更新钟表表盘的时区 update timezone of clock face
    
    # change clock face which related the 'Theme' button
    def change_clock_face(self):
        options = QFileDialog.Option

        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self, "Select Clock Face Image", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
                                                   options=QFileDialog.Option)
    
        if file_name:
            self.clock_widget.set_clock_face(file_name)

    def show_alarm_window(self):
        self.alarm_window = AlarmWindow(self)
        self.alarm_window.show()
        
    # 显示或隐藏日历 show or hide calendar
    def toggle_calendar(self):
        if self.calendar_mini.isVisible():
            self.calendar_mini.setVisible(False)
            self.toggle_calendar_button.setText('show calendar')
        else:
            self.calendar_mini.setStyleSheet('background-color: yellow')
            self.calendar_mini.setVisible(True)
            self.toggle_calendar_button.setText('hide calendar')

class ClockWidget(QWidget):
    def __init__(self, parent=None):
        super(ClockWidget, self).__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        self.timezone = tz.tzlocal()  # 默认使用本地时区 default to local timezone

    def set_timezone(self, timezone):
        self.timezone = timezone
        self.update()  # 立即更新钟表表盘 immediately update clock face

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        self.draw_clock(painter)
        painter.end()

    # change face of clock
    def set_clock_face(self, image_path):
        self.clock_face = QPixmap(image_path)
        self.update()  # 立即更新钟表表盘

    def draw_clock(self, painter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center_x = self.width() / 2
        center_y = self.height() / 3.5
        #  print(center_x, center_y)
        clock_radius = min(self.width(), self.height()) / 4
        painter.translate(center_x, center_y)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 绘制表盘 draw clock face
        gradient = QRadialGradient(0, 0, clock_radius)
        gradient.setColorAt(0, QColor(20, 0, 40))
        gradient.setColorAt(1, QColor(207, 217, 233))
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(int(-clock_radius), int(-clock_radius), int(2 * clock_radius), int(2 * clock_radius))

        # 绘制刻度和数字 drwa scale and number
        for i in range(12):
            angle = -(i + 10) * 30
            x = clock_radius * 0.8 * math.cos(math.radians(angle))
            y = -clock_radius * 0.8 * math.sin(math.radians(angle))

            # 创建 QPoint 对象
            text_x = int(x - 10)  # 调整数字的水平位置
            text_y = int(y + 10)  # 调整数字的垂直位置
            text_position = QPoint(text_x, text_y)

            # 绘制数字
            painter.drawText(text_position, str(i + 1))

            # 绘制刻度
            line_x = int(clock_radius * 0.6 * math.cos(math.radians(angle)))
            line_y = int(-clock_radius * 0.6 * math.sin(math.radians(angle)))
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawLine(line_x, line_y, int(x), int(y))

        # 获取当前时间 get current time
        current_time = datetime.now(self.timezone).time()
        secs = current_time.second
        mins = current_time.minute + secs / 60
        hrs = current_time.hour + mins / 60

        # 绘制时针 draw hour hand
        painter.setPen(QPen(QColor(50, 50, 50), 6))
        painter.setBrush(QColor(50, 50, 50))
        painter.rotate(hrs * (360 / 12))
        painter.drawRect(-5, int (-clock_radius / 2), 10, int(clock_radius / 2))  # 使用矩形作为时针
        painter.rotate(-hrs * (360 / 12))

        # 绘制分针 draw minute hand
        painter.setPen(QPen(QColor(0, 0, 0), 4))
        painter.rotate(mins * (360 / 60))
        painter.drawLine(0, 0, 0, round(-clock_radius * 0.7))
        painter.rotate(-mins * (360 / 60))

        # 绘制秒针 draw second hand
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.rotate(secs * (360 / 60))
        painter.drawLine(0, 0, 0, round(-clock_radius * 0.9))
        painter.rotate(-secs * (360 / 60))

        painter.restore()

class AlarmWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.time_edit = QTimeEdit(self)
        layout.addWidget(self.time_edit)

        self.music_combo = QComboBox(self)
        self.music_combo.addItem("Select a Music")
        self.music_combo.addItem("Music 1", "path/to/music1.mp3")
        self.music_combo.addItem("Music 2", "path/to/music2.mp3")
        layout.addWidget(self.music_combo)

        self.set_button = QPushButton('Set Alarm', self)
        self.set_button.clicked.connect(self.set_alarm)
        layout.addWidget(self.set_button)

        self.setWindowTitle('Set Alarm')
        self.setGeometry(100, 100, 200, 150)

    def set_alarm(self):
        time = self.time_edit.time()
        music_path = self.music_combo.currentData()
        if music_path:
            print(f"Alarm set to {time.toString()} with music {music_path}")
            # 在这里添加代码来设置实际的闹钟
            self.close()
        else:
            print("Please select a music.")

class CalendarWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget(self)
        # self.calendar.setStyleSheet('background-image: url(你的图片路径); background-repeat: no-repeat; background-position: center')

        self.layout.addWidget(self.calendar)
        self.setLayout(self.layout)

        self.setGeometry(100, 100, 640, 480)  # 设置窗口的位置和大小
        self.setWindowTitle('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TalkingClockApp()
    ex.show()
    ex.setGeometry(100, 100, 600, 600)
    sys.exit(app.exec())
