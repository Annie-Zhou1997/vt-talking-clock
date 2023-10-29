import sys
import os
import pytz
import math
import warnings
import pygame
warnings.filterwarnings("ignore", category=RuntimeWarning)
from pydub import AudioSegment
from PyQt6.QtCore import QTimer, Qt, QDate, QPoint, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient, QPixmap, QPainterPath, QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QCheckBox,
                             QComboBox, QStylePainter, QStyle, QStyleOptionComboBox,
                             QGridLayout, QFileDialog, QSlider)
from gtts import gTTS
from tzlocal import get_localzone_name
from datetime import datetime
from dateutil import tz
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

        self.date_timer = QTimer(self)
        self.date_timer.timeout.connect(self.update_date)
        self.date_timer.start(86400000)

    def init_ui(self):
        layout = QGridLayout(self)
        self.setWindowTitle('Talking Clock')
        self.setWindowIcon(QIcon('art.jpg'))
        self.setFixedSize(600, 600)

        # 日期标签 date label
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("QLabel { font-size: 30px}")
        self.date_label.setGeometry(160, 320, 290, 60)
        self.update_date()

        self.clock_widget = ClockWidget(self)
        layout.addWidget(self.clock_widget, 0, 0, 1, 3)

        # 电子时钟标签 electronic clock label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { font-size: 50px; }")
        self.label.setGeometry(150, 370, 300, 50)  #  position and size of  clock

        # Theme button
        self.change_clock_face_button = QPushButton('Theme', self)
        self.change_clock_face_button.setGeometry(480, 10, 100, 30)
        self.change_clock_face_button.clicked.connect(self.change_clock_face)

        # Timezone combo box
        self.timezone_combo = CustomComboBox(self)
        self.timezone_combo.addItem(str(self.timezone))
        self.timezone_combo.addItem("Europe/London")
        self.timezone_combo.addItem("Europe/Moscow")
        self.timezone_combo.addItem("America/New_York")
        self.timezone_combo.addItem("Asia/Shanghai")
        self.timezone_combo.addItem("UTC")

        self.timezone_combo.setGeometry(10, 10, 190, 30)
        self.timezone_combo.currentIndexChanged.connect(self.update_timezone)

        self.play_button_en = QPushButton('English', self)
        self.play_button_en.setGeometry(250, 430, 100, 30)
        self.play_button_en.clicked.connect(self.play_time_en)

        self.play_button_zh = QPushButton('中文', self)
        self.play_button_zh.setGeometry(250, 470, 100, 30)
        self.play_button_zh.clicked.connect(self.play_time_zh)

        self.play_button_ru = QPushButton('Русский', self)
        self.play_button_ru.setGeometry(250, 510, 100, 30)
        self.play_button_ru.clicked.connect(self.play_time_ru)

        self.play_button_nl = QPushButton('Nederlands', self)
        self.play_button_nl.setGeometry(250, 550, 100, 30)
        self.play_button_nl.clicked.connect(self.play_time_nl)

        # 24-hour format checkbox
        self.format_checkbox = QCheckBox('24 Hour Format', self)
        self.format_checkbox.setGeometry(20, 555, 200, 30)
        self.format_checkbox.stateChanged.connect(self.update_format)

        self.tt = QLabel("Voice speed:", self)
        self.tt.setStyleSheet("QLabel { font-size:16px; font-family: Calibri}")
        self.tt.move(400, 510)

        self.zerox = QLabel("0", self)
        self.zerox.setStyleSheet("QLabel { font-size:12px; font-family: Calibri}")
        self.zerox.move(400, 560)

        self.onex = QLabel("1x", self)
        self.onex.setStyleSheet("QLabel { font-size:12px; font-family: Calibri}")
        self.onex.move(467, 560)

        self.twox = QLabel("2x", self)
        self.twox.setStyleSheet("QLabel { font-size:12px; font-family: Calibri}")
        self.twox.move(540, 560)

        self.mySlider = QSlider(Qt.Orientation.Horizontal, self)
        self.mySlider.setGeometry(400, 540, 150, 30)
        self.mySlider.setMinimum(10)
        self.mySlider.setMaximum(200)
        self.mySlider.setValue(100)
        self.mySlider.setStyleSheet("QSlider { border-size:10px; }")
        self.mySlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.mySlider.setTickInterval(10)

        with open("clock.stylesheet", "r") as fh:
            self.setStyleSheet(fh.read())

    def update_date(self):
        current_date = QDate.currentDate()
        self.date_label.setText(current_date.toString("yyyy-MM-dd dddd"))

    def show_time(self):
        timezone = pytz.timezone(self.timezone_combo.currentText())
        current_time = datetime.now(timezone).strftime('%I:%M %p' if not self.format_24hr else '%H:%M')
        self.label.setText(current_time)

    @staticmethod
    def speed_change(sound, speed=1.0):
        return sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})

    def play_time(self, lang):
        timezone = pytz.timezone(self.timezone_combo.currentText())
        current_time = datetime.now(timezone).strftime("%H:%M")
        hours, minutes = current_time.split(':')

        result_audio = AudioSegment.empty()
        if lang in ['ru', 'zh', 'en']:
            if lang == 'ru':
                synthesized = ru_convert(current_time)
                audio_files = ['current_time.wav'] + synthesized
                for file_path in audio_files:
                    audio_segment = AudioSegment.from_file('Russian/' + file_path)
                    result_audio += audio_segment
            elif lang == 'zh':
                hour, minute = int(hours), int(minutes)
                audio_files = ['current_time.wav'] + ch_convert(hour) + ['point.wav']
                if minute == 0:
                    audio_files += ['o_clock.wav']
                elif minute == 30:
                    audio_files += ['half.wav']
                else:
                    audio_files += ch_convert(minute) + ['minute.wav']
                for file_path in audio_files:
                    audio_segment = AudioSegment.from_file('Chinese/' + file_path)
                    result_audio += audio_segment
            elif lang == 'en':
                hour, minute = int(hours), int(minutes)
                time_suffix = ['en_PM.WAV'] if hour >= 12 else ['en_AM.WAV']
                if hour > 12:
                    hour -= 12
                if minute == 0:
                    audio_files = ['current_time.wav'] + en_convert(hour) + ['en_o_clock.WAV'] + time_suffix
                elif minute == 15:
                    audio_files = ['current_time.wav'] + ['en_quarter_past.WAV'] + en_convert(hour) + time_suffix
                elif minute == 30:
                    audio_files = ['current_time.wav'] + ['en_half_past.WAV'] + en_convert(hour) + time_suffix
                elif minute == 45:
                    audio_files = ['current_time.wav'] + ['en_quarter_to.WAV'] + en_convert(
                        1 if hour == 12 else hour + 1) + time_suffix
                else:
                    minutes_audio = en_convert(minute)
                    audio_files = ['current_time.wav'] + en_convert(hour) + minutes_audio + time_suffix

                for file_path in audio_files:
                    if isinstance(file_path, list):
                        for fp in file_path:
                            audio_segment = AudioSegment.from_file('English/' + fp)
                            result_audio += audio_segment
                    else:
                        audio_segment = AudioSegment.from_file('English/' + file_path)
                        result_audio += audio_segment
        else:
            prefixes = {'nl': 'De huidige tijd is'}
            time_text = datetime.now(timezone).strftime('%I:%M %p' if not self.format_24hr else '%H:%M')
            text_to_speak = f"{prefixes[lang]} {time_text}"
            tts = gTTS(text=text_to_speak, lang=lang)
            tts.save("time.mp3")
            result_audio = AudioSegment.from_file("time.mp3")
        result_audio = self.speed_change(result_audio, self.mySlider.value() / 100)
        result_audio.export("current_time.wav", format="wav")
        pygame.init()
        pygame.mixer.music.load("current_time.wav")
        pygame.mixer.music.play()
        pygame.time.wait(int(result_audio.duration_seconds * 1000))
        pygame.quit()
        if os.path.exists('current_time.wav'): os.remove('current_time.wav')
        if os.path.exists('time.mp3'): os.remove('time.mp3')

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
        self.clock_widget.set_timezone(self.timezone)

    # change clock face which related the 'Theme' button
    def change_clock_face(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self, "Select Clock Face Image", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
        if file_name:
            with open('config.ini', 'w', encoding='utf-8') as f:
                f.writelines(["[CLOCK_FACE]\n", file_name])
            self.clock_widget.update()


class ClockWidget(QWidget):
    def __init__(self, parent=None):
        super(ClockWidget, self).__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        self.timezone = tz.tzlocal()  # default to local timezone

    def set_timezone(self, timezone):
        self.timezone = timezone
        self.update()  # immediately update clock face

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)

        with open('config.ini', 'r',  encoding='utf-8') as f:
            config = f.readlines()
        self.draw_clock(painter, 'image', config[1]) if len(config) > 1 else (
            self.draw_clock(painter, 'gradient', None))
        painter.end()

    def draw_clock(self, painter, mode, dir):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center_x = self.width() / 2
        center_y = self.height() / 3.5

        clock_radius = min(self.width(), self.height()) / 4
        painter.translate(center_x, center_y)

        if mode == 'gradient':
            gradient = QRadialGradient(0, 0, clock_radius)
            gradient.setColorAt(0, QColor(20, 0, 40))
            gradient.setColorAt(1, QColor(207, 217, 233))
            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawEllipse(int(-clock_radius), int(-clock_radius), int(2 * clock_radius), int(2 * clock_radius))
        elif mode == 'image':
            background_image = QPixmap(dir)
            clip_path = QPainterPath()
            clip_path.addEllipse(QPointF(0, 0), clock_radius, clock_radius)
            painter.setClipPath(clip_path)
            painter.drawPixmap(int(-clock_radius), int(-clock_radius), int(2 * clock_radius), int(2 * clock_radius), background_image)

        # Draw the clock hands, ticks, and numbers
        for i in range(12):
            angle = -(i + 10) * 30
            x = clock_radius * math.cos(math.radians(angle))
            y = -clock_radius * math.sin(math.radians(angle))

            # Create QPoint object
            text_x, text_y = int(x * 0.8), int(y * 0.8)
            text_position = QPoint(text_x, text_y)

            # Draw number
            painter.drawText(text_position, str(i + 1))

            # Draw scale (tick)
            line_x = int(clock_radius * 0.9 * math.cos(math.radians(angle)))
            line_y = int(-clock_radius * 0.9 * math.sin(math.radians(angle)))
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawLine(line_x, line_y, int(x), int(y))

        # Get current time
        current_time = datetime.now(self.timezone).time()
        secs = current_time.second
        mins = current_time.minute + secs / 60
        hrs = current_time.hour + mins / 60

        # Draw hour hand
        painter.setPen(QPen(QColor(50, 50, 50), 6))
        painter.setBrush(QColor(50, 50, 50))
        painter.rotate(hrs * (360 / 12))
        painter.drawRect(-5, int(-clock_radius / 2), 10, int(clock_radius / 2))
        painter.rotate(-hrs * (360 / 12))

        # Draw minute hand
        painter.setPen(QPen(QColor(0, 0, 0), 4))
        painter.rotate(mins * (360 / 60))
        painter.drawLine(0, 0, 0, round(-clock_radius * 0.7))
        painter.rotate(-mins * (360 / 60))

        # Draw second hand
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.rotate(secs * (360 / 60))
        painter.drawLine(0, 0, 0, round(-clock_radius * 0.9))
        painter.rotate(-secs * (360 / 60))
        painter.restore()

        painter.setClipPath(QPainterPath())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TalkingClockApp()
    ex.show()
    ex.setGeometry(420, 155, 600, 600)
    sys.exit(app.exec())
