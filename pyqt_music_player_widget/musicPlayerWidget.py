import os

from mutagen import mp3
import librosa

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

    def __init__(self, title=False, title_file_ext=True, slider=None, control_alignment=Qt.AlignCenter, volume=True):
        super().__init__()
        self.__title_file_ext = title_file_ext
        self.__initUi(control_alignment, title, slider, volume)

    def __initUi(self, control_alignment, title, slider=None, volume=False, volume_width=100):
        self.__mediaPlayer = QMediaPlayer()
        self.__mediaPlayer.setNotifyInterval(1)

        self.__timerLbl = QLabel()
        self.__curLenLbl = QLabel()
        self.__slash = QLabel()

        self.__slider = slider if slider else MediaSlider()
        self.__slider.pressed.connect(self.__handlePressed)
        self.__slider.dragged.connect(self.__handleDragged)
        self.__slider.released.connect(self.__handleReleased)

        self.__zeroTimeStr = '00:00:00'

        self.__timerLbl.setText(self.__zeroTimeStr)
        self.__curLenLbl.setText(self.__zeroTimeStr)
        self.__slash.setText("/")

        lay = QHBoxLayout()
        lay.addWidget(self.__slider)
        lay.addWidget(self.__timerLbl)
        lay.addWidget(self.__slash)
        lay.addWidget(self.__curLenLbl)

        if volume:
            self.__volume = 100
            self.__mute = False

            self.__volume_slider = MediaSlider()
            self.__volume_slider.setFixedWidth(volume_width)
            self.__volume_slider.setSliderPosition(self.__volume * 100)
            self.__volume_slider.released.connect(self.__volumeChanged)
            self.__volume_slider.dragged.connect(self.__volumeChanged)

            self.__muteBtn = SvgButton()
            self.__muteBtn.setIcon('ico/volume.svg')
            self.__muteBtn.setObjectName('mute')

            self.__muteBtn.clicked.connect(self.__toggleMute)

            lay.addWidget(self.__muteBtn)
            lay.addWidget(self.__volume_slider)

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
        lay.setAlignment(control_alignment)
        for btn in btns:
            lay.addWidget(btn)

        self.__title_label = None
        if title:
            self.__title_label = QLabel()
            self.__title_label.setAlignment(control_alignment | Qt.AlignmentFlag.AlignCenter)
            lay.addWidget(self.__title_label)

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
        _filename = filename.lower()
        if _filename.endswith(".mp3"):
            audio = mp3.MP3(filename)
            media_length = audio.info.length
        elif _filename.endswith(".wav"):
            media_length = librosa.get_duration(path=filename)
        else:
            raise TypeError(f"{filename} has unsupported file format")

        # convert second into hh:mm:ss
        h = int(media_length / 3600)
        media_length -= (h * 3600)
        m = int(media_length / 60)
        media_length -= (m * 60)
        s = media_length
        song_length = '{:0>2d}:{:0>2d}:{:0>2d}'.format(int(h), int(m), int(s))

        return song_length

    def __volumeChanged(self, pos):
        self.__volume = pos // 100
        self.__mediaPlayer.setVolume(self.__volume)

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
        if self.__title_label:
            _, name = os.path.split(filename)
            if self.__title_file_ext:
                self.__title_label.setText(name.split(".")[0])
            else:
                self.__title_label.setText(name)

    def cleanTitle(self):
        if self.__title_label:
            self.__title_label.setText('')

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

    def __toggleMute(self):
        self.__mute = not self.__mute
        self.__volume_slider.setEnabled(not self.__mute)

        if self.__mute:
            self.__volume_slider.setSliderPosition(0)
            self.__mediaPlayer.setVolume(0)
            self.__muteBtn.setIcon('ico/mute.svg')
        else:
            self.__volume_slider.setSliderPosition(self.__volume * 100)
            self.__mediaPlayer.setVolume(self.__volume)
            self.__muteBtn.setIcon('ico/volume.svg')

        self.__muteBtn.setObjectName('mute')

    def stop(self):
        self.__playBtn.setIcon('ico/play.svg')
        self.__playBtn.setObjectName('play')
        self.__mediaPlayer.stop()
        self.__stopBtn.setEnabled(False)
        self.played.emit(False)