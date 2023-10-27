import sys
import os
import pytz
import math
import warnings
import pygame

warnings.filterwarnings("ignore", category=RuntimeWarning)
from pydub import AudioSegment
from PyQt6.QtCore import QTimer, QTime, Qt, QDate, QPoint
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient, QPixmap
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
                             QTimeEdit, QMessageBox, QComboBox, QStylePainter, QStyle, QStyleOptionComboBox,
                             QGridLayout, QFileDialog, QCalendarWidget)
from gtts import gTTS
from tzlocal import get_localzone_name
from datetime import datetime
from dateutil import tz
from playsound import playsound
from Russian import *
from Chinese import *
from English import *


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
        self.timezone = pytz.timezone(get_localzone_name())
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
        self.setWindowTitle('Talking Clock')
        self.setFixedSize(600, 600)

        # 日期标签 date label
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("QLabel { font-size: 22px; }")
        self.date_label.setGeometry(180, 320, 250, 60)  # 你可以根据需要调整位置和大小
        self.update_date()

        self.clock_widget = ClockWidget(self)
        layout.addWidget(self.clock_widget, 0, 0, 1, 3)

        # 电子时钟标签 electronic clock label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { font-size: 40px; }")
        self.label.setGeometry(150, 380, 300, 50)  # 设置电子时钟的位置和大小 set position and size of electronic clock

        self.play_button = QPushButton('English', self)
        self.play_button.setGeometry(250, 430, 100, 30)
        self.play_button.clicked.connect(self.play_time_en)

        self.play_button_zh = QPushButton('中文', self)
        self.play_button_zh.setGeometry(250, 470, 100, 30)
        self.play_button_zh.clicked.connect(self.play_time_zh)

        self.play_button_ru = QPushButton('Русский', self)
        self.play_button_ru.setGeometry(250, 510, 100, 30)
        self.play_button_ru.clicked.connect(self.play_time_ru)

        self.play_button_nl = QPushButton('Nederlands', self)
        self.play_button_nl.setGeometry(250, 550, 100, 30)
        self.play_button_nl.clicked.connect(self.play_time_nl)

        # Theme button
        self.change_clock_face_button = QPushButton('Theme', self)
        self.change_clock_face_button.setGeometry(400, 470, 100, 30)
        self.change_clock_face_button.clicked.connect(self.change_clock_face)

        # Timezone combo box
        self.timezone_combo = CustomComboBox(self)
        self.timezone_combo.addItem("UTC")
        self.timezone_combo.addItem("America/New_York")
        self.timezone_combo.addItem("Europe/Amsterdam")
        self.timezone_combo.addItem("Europe/London")
        self.timezone_combo.addItem("Europe/Moscow")
        self.timezone_combo.addItem("Asia/Shanghai")
        self.timezone_combo.setGeometry(10, 10, 190, 30)
        self.timezone_combo.currentIndexChanged.connect(self.update_timezone)

        # 24-hour format checkbox
        self.format_checkbox = QCheckBox('24 Hour Format', self)
        self.format_checkbox.setGeometry(20, 560, 200, 30)
        self.format_checkbox.stateChanged.connect(self.update_format)

        # Set Alarm button
        self.alarm_button = QPushButton('Set Alarm', self)
        self.alarm_button.setGeometry(480, 10, 100, 30)
        self.alarm_button.clicked.connect(self.show_alarm_window)

        # Full Calendar button
        self.toggle_calendar_button = QPushButton('Calendar', self)
        self.toggle_calendar_button.setGeometry(480, 50, 100, 30)
        self.toggle_calendar_button.clicked.connect(self.toggle_calendar)

        with open("clock.stylesheet", "r") as fh:
            self.setStyleSheet(fh.read())

    def open_full_calendar(self):
        self.calendar_window = CalendarWindow()
        self.calendar_window.show()

    def update_date(self):
        current_date = QDate.currentDate()
        self.date_label.setText(current_date.toString("yyyy-MM-dd dddd"))

    def show_time(self):
        timezone = pytz.timezone(self.timezone_combo.currentText())
        current_time = datetime.now(timezone)

        time_format = '%I:%M %p' if not self.format_24hr else '%H:%M'
        time_text = current_time.strftime(time_format)
        self.label.setText(time_text)

    def play_time(self, lang='en'):
        timezone = pytz.timezone(self.timezone_combo.currentText())
        current_time = datetime.now(timezone)
        time_text = current_time.strftime('%I:%M %p' if not self.format_24hr else '%H:%M')
        current_time = current_time.strftime("%H:%M")
        hours, minutes = current_time.split(':')
        result_audio = AudioSegment.empty()
        if lang in ['ru', 'zh', 'en']:
            if lang == 'ru':
                hours_audio = ru_convert(int(hours), 'h')
                minutes_audio = ru_convert(int(minutes), 'm')
                audio_files = ['current_time.wav'] + hours_audio + minutes_audio

                for file_path in audio_files:
                    audio_segment = AudioSegment.from_file('Russian/' + file_path)
                    result_audio += audio_segment

            elif lang == 'zh':
                hours_audio = ch_convert(int(hours))
                minutes_audio = ch_convert(int(minutes))
                audio_files = ['current_time.wav'] + hours_audio + ['point.wav'] + minutes_audio + ['minute.wav']

                for file_path in audio_files:
                    audio_segment = AudioSegment.from_file('Chinese/' + file_path)
                    result_audio += audio_segment

            elif lang == 'en':
                result_en = ['current_time.wav']
                if int(hours) <= 12:
                    hours_audio = en_convert(int(hours))
                    time_suffix = ['en_AM.WAV']
                else:
                    hours_audio = en_convert(int(hours) - 12)
                    time_suffix = ['en_PM.WAV']
                minutes_audio = en_convert(int(minutes))
                audio_files = ['current_time.wav'] + hours_audio + minutes_audio + time_suffix

                for file_path in audio_files:
                    audio_segment = AudioSegment.from_file('English/' + file_path)
                    result_audio += audio_segment

            result_audio.export("current_time.wav", format="wav")
            pygame.init()
            pygame.mixer.music.load("current_time.wav")
            pygame.mixer.music.play()
            pygame.mixer.music.play()
            pygame.time.wait(int(result_audio.duration_seconds * 1000))
            pygame.quit()
            os.remove("current_time.wav")

        else:
            prefixes = {'nl': 'De huidige tijd is'}

            text_to_speak = f"{prefixes[lang]} {time_text}"
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

    def update_format(self):
        self.format_24hr = self.format_checkbox.isChecked()

    def update_timezone(self):
        self.timezone = pytz.timezone(self.timezone_combo.currentText())
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

        # 绘制刻度和数字 draw scale and number
        for i in range(12):
            angle = -(i + 10) * 30
            x = clock_radius * math.cos(math.radians(angle))
            y = -clock_radius * math.sin(math.radians(angle))

            # 创建 QPoint 对象
            text_x = int(x * 0.8)  # 调整数字的水平位置
            text_y = int(y * 0.8)  # 调整数字的垂直位置
            text_position = QPoint(text_x, text_y)

            # 绘制数字
            painter.drawText(text_position, str(i + 1))

            # 绘制刻度
            line_x = int(clock_radius * 0.9 * math.cos(math.radians(angle)))
            line_y = int(-clock_radius * 0.9 * math.sin(math.radians(angle)))
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
        painter.drawRect(-5, int(-clock_radius / 2), 10, int(clock_radius / 2))  # 使用矩形作为时针
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


# setting alarm
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

        self.set_button = QPushButton('Alarm', self)
        self.set_button.clicked.connect(self.set_alarm)
        layout.addWidget(self.set_button)

        self.setStyleSheet("background-color: lightblue;")

        self.setWindowTitle('Set Alarm')
        self.setGeometry(400, 200, 170, 250)

    def set_alarm(self):
        time = self.time_edit.time()
        music_path = self.music_combo.currentData()
        if music_path:
            current_time = QTime.currentTime()  # Get the current time
            alarm_time = time

            # Calculate the time until the alarm goes off
            time_until_alarm = current_time.secsTo(alarm_time)
            if time_until_alarm > 0:
                # Schedule the alarm to play the music
                alarm_timer = QTimer()
                alarm_timer.timeout.connect(lambda: self.play_alarm(music_path, alarm_timer))
                alarm_timer.start(time_until_alarm * 1000)  # QTimer works in milliseconds
            else:
                QMessageBox.critical(self, "Invalid Alarm Time", "Please select a future time for the alarm.")
        else:
            QMessageBox.critical(self, "No Music Selected", "Please select a music.")

    def play_alarm(self, music_path, timer):
        print("Alarm triggered! Playing music...")
        try:
            playsound(music_path)
        except Exception as e:
            QMessageBox.critical(self, "Error Playing Music", f"An error occurred: {str(e)}")
        finally:
            timer.stop()


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
