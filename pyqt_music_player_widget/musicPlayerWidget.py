from mutagen import mp3

from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from pyqt_music_slider.musicSlider import MusicSlider
from pyqt_svg_icon_pushbutton.svgIconPushButton import SvgIconPushButton
from PyQt5.QtCore import Qt


class MusicPlayerWidget(QWidget):
    played = pyqtSignal(bool)

    def __init__(self, slider=None):
        super().__init__()
        self.__initUi(slider)

    def __initUi(self, slider=None):
        self.__mediaPlayer = QMediaPlayer()
        self.__mediaPlayer.setNotifyInterval(1)

        self.__timer_lbl = QLabel()
        self.__cur_len_lbl = QLabel()

        self.__slider = slider if slider else MusicSlider()
        self.__slider.updatePosition.connect(self.updatePosition)

        self.__timer_lbl.setText('00:00:00')
        self.__cur_len_lbl.setText('00:00:00')

        lay = QHBoxLayout()
        lay.addWidget(self.__timer_lbl)
        lay.addWidget(self.__slider)
        lay.addWidget(self.__cur_len_lbl)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__playBtn = SvgIconPushButton()
        self.__playBtn.setIcon('ico/play.svg')
        self.__playBtn.setEnabled(False)

        self.__stopBtn = SvgIconPushButton()
        self.__stopBtn.setIcon('ico/stop.svg')
        self.__stopBtn.setEnabled(False)

        btns = [self.__playBtn, self.__stopBtn]

        self.__playBtn.clicked.connect(self.togglePlayback)
        self.__stopBtn.clicked.connect(self.stop)

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignCenter)
        for btn in btns:
            lay.addWidget(btn)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(bottomWidget)
        lay.setContentsMargins(2, 2, 2, 2)

        self.setLayout(lay)

        self.__slider.seeked.connect(self.setPosition)
        self.__mediaPlayer.positionChanged.connect(self.updatePosition)
        self.__mediaPlayer.durationChanged.connect(self.updateDuration)

    def __getMediaLengthHumanFriendly(self, filename):
        audio = mp3.MP3(filename)
        media_length = audio.info.length

        # convert second into hh:mm:ss
        h = int(media_length / 3600)
        media_length -= (h * 3600)
        m = int(media_length / 60)
        media_length -= (m * 60)
        s = media_length
        song_length = '{:0>2d}:{:0>2d}:{:0>2d}'.format(int(h), int(m), int(s))

        return song_length

    def setPosition(self, pos):
        # if (qAbs(self.__mediaPlayer.position()) - pos) > 99:
        self.__mediaPlayer.setPosition(pos)

    # convert millisecond into hh:mm:ss
    def formatTime(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = round(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24

        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def updatePosition(self, pos):
        self.__slider.setValue(pos)
        self.__timer_lbl.setText(self.formatTime(pos))

    def updateDuration(self, duration):
        self.__slider.setRange(0, duration)
        self.__slider.setEnabled(duration > 0)
        self.__slider.setPageStep(duration / 1000)

    def setMedia(self, filename):
        mediaContent = QMediaContent(QUrl.fromLocalFile(filename))  # it also can be used as playlist
        self.__mediaPlayer.setMedia(mediaContent)
        self.__playBtn.setEnabled(True)
        self.__cur_len_lbl.setText(self.__getMediaLengthHumanFriendly(filename))

    def play(self):
        self.__playBtn.setIcon('ico/pause.svg')
        self.__mediaPlayer.play()
        self.played.emit(True)
        self.__stopBtn.setEnabled(True)

    def pause(self):
        self.__playBtn.setIcon('ico/play.svg')
        self.__mediaPlayer.pause()

    def togglePlayback(self):
        if self.__mediaPlayer.mediaStatus() == QMediaPlayer.NoMedia:
            pass # or openFile()
        elif self.__mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def stop(self):
        self.__playBtn.setIcon('ico/play.svg')
        self.__mediaPlayer.stop()
        self.__stopBtn.setEnabled(False)
        self.played.emit(False)