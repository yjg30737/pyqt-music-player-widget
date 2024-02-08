# pyqt-music-player-widget
PyQt music player widget

## Requirements
PyQt5 >= 5.8

## Setup
`python -m pip install git+https://github.com/nikonru/pyqt-music-player-widget --upgrade`

## Included Packages
* <a href="https://github.com/beetbox/audioread.git">audioread</a>
* <a href="https://github.com/yjg30737/pyqt-media-slider.git">pyqt-media-slider</a>
* <a href="https://github.com/yjg30737/pyqt-svg-button.git">pyqt-svg-button</a>

This is using `audioread` to get the full length of the media.

## Method/Signal Overview
* Methods - `play()`, `pause()`, `stop()`
* Signals - `played(bool)`, `positionUpdated(int)`, `durationUpdated(int)`

## Example
```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QFormLayout

from pyqt_music_player_widget import MusicPlayerWidget


class MusicPlayerExample(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):

        lay = QFormLayout()
        lay.setContentsMargins(0, 0, 0, 0)

        self.__musicPlayerWidget = MusicPlayerWidget()

        lay = QVBoxLayout()
        lay.addWidget(self.__musicPlayerWidget)

        self.setLayout(lay)
        self.__musicPlayerWidget.setMedia("./music.mp3")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    player = MusicPlayerExample()
    player.show()
    sys.exit(app.exec_())
```
