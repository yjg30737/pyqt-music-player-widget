from mutagen import mp3

from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout

from pyqt_media_slider.mediaSlider import MediaSlider
from pyqt_svg_button.svgButton import SvgButton
from PyQt5.QtCore import Qt


class MusicPlayerWidget(QWidget):
    played = pyqtSignal(bool)
    positionUpdated = pyqtSignal(int)
    durationUpdated = pyqtSignal(int)

    def __init__(self, slider=None):
        super().__init__()
        self.__initUi(slider)

    def __initUi(self, slider=None):
        self.__mediaPlayer = QMediaPlayer()
        self.__mediaPlayer.setNotifyInterval(1)

        self.__timerLbl = QLabel()
        self.__curLenLbl = QLabel()

        self.__slider = slider if slider else MediaSlider()
        self.__slider.pressed.connect(self.__handlePressed)
        self.__slider.dragged.connect(self.__handleDragged)
        self.__slider.released.connect(self.__handleReleased)

        self.__zeroTimeStr = '00:00:00'

        self.__timerLbl.setText(self.__zeroTimeStr)
        self.__curLenLbl.setText(self.__zeroTimeStr)

        lay = QHBoxLayout()
        lay.addWidget(self.__timerLbl)
        lay.addWidget(self.__slider)
        lay.addWidget(self.__curLenLbl)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__playBtn = SvgButton()
        self.__playBtn.setIcon('ico/play.svg')
        self.__playBtn.setObjectName('play')
        self.__playBtn.setEnabled(False)

        self.__stopBtn = SvgButton()
        self.__stopBtn.setIcon('ico/stop.svg')
        self.__stopBtn.setEnabled(False)

        btns = [self.__playBtn, self.__stopBtn]

        self.__playBtn.clicked.connect(self.__togglePlayback)
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

        self.__mediaPlayer.positionChanged.connect(self.__updatePosition)
        self.__mediaPlayer.durationChanged.connect(self.__updateDuration)

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

    def __handlePressed(self, pos):
        self.__mediaPlayer.pause()
        self.__setPosition(pos)

    def __handleDragged(self, pos):
        self.__timerLbl.setText(self.__formatTime(pos))

    def __handleReleased(self, pos):
        self.__setPosition(pos)
        if self.__playBtn.objectName() == 'play':
            pass
        else:
            self.__mediaPlayer.play()

    def __setPosition(self, pos):
        self.__mediaPlayer.setPosition(pos)

    # convert millisecond into hh:mm:ss
    def __formatTime(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24

        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def __updatePosition(self, pos):
        self.__slider.setValue(pos)
        if pos == self.__slider.maximum():
            self.stop()
        self.__timerLbl.setText(self.__formatTime(pos))
        self.positionUpdated.emit(pos)

    def __updateDuration(self, duration):
        self.__slider.setRange(0, duration)
        self.__slider.setEnabled(duration > 0)
        self.__slider.setPageStep(duration // 1000)
        self.durationUpdated.emit(duration)

    def setMedia(self, filename):
        mediaContent = QMediaContent(QUrl.fromLocalFile(filename))  # it also can be used as playlist
        self.__mediaPlayer.setMedia(mediaContent)
        self.__playBtn.setEnabled(True)
        self.__curLenLbl.setText(self.__getMediaLengthHumanFriendly(filename))

    def getCurrentMediaPosition(self):
        return self.__mediaPlayer.position()

    def getCurrentMediaLength(self):
        return self.__slider.maximum()

    def play(self):
        self.__playBtn.setIcon('ico/pause.svg')
        self.__playBtn.setObjectName('pause')
        self.__mediaPlayer.play()
        self.played.emit(True)
        self.__stopBtn.setEnabled(True)

    def pause(self):
        self.__playBtn.setIcon('ico/play.svg')
        self.__playBtn.setObjectName('play')
        self.__mediaPlayer.pause()

    def __togglePlayback(self):
        if self.__mediaPlayer.mediaStatus() == QMediaPlayer.NoMedia:
            pass  # or openFile()
        elif self.__mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def stop(self):
        self.__playBtn.setIcon('ico/play.svg')
        self.__playBtn.setObjectName('play')
        self.__mediaPlayer.stop()
        self.__stopBtn.setEnabled(False)
        self.played.emit(False)