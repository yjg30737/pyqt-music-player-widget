# pyqt-music-player-widget
PyQt music player widget

## Requirements
PyQt5 >= 5.8

## Setup
`pip3 install git+https://github.com/yjg30737/pyqt-music-player-widget --upgrade`

## Included Packages
* <a href="https://mutagen.readthedocs.io/en/latest/index.html">mutagen</a>
* <a href="https://github.com/yjg30737/pyqt-media-slider.git">pyqt-media-slider</a>
* <a href="https://github.com/yjg30737/pyqt-svg-button.git">pyqt-svg-button</a>

This is using `Mutagen` to get the full length of the media.

This only works for mp3 extension.

## Example
```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QFormLayout
from pyqt_find_path_widget import FindPathWidget

from pyqt_music_player_widget import MusicPlayerWidget


class MusicPlayerExample(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__findPathWidget = FindPathWidget() # https://github.com/yjg30737/pyqt-find-path-widget.git
        self.__findPathWidget.setExtOfFiles('Audio Files (*.mp3)')
        self.__findPathWidget.added.connect(self.__added)

        lay = QFormLayout()
        lay.addRow('Audio File', self.__findPathWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        pathFindWidget = QWidget()
        pathFindWidget.setLayout(lay)

        self.__musicPlayerWidget = MusicPlayerWidget()

        lay = QVBoxLayout()
        lay.addWidget(pathFindWidget)
        lay.addWidget(self.__musicPlayerWidget)

        self.setLayout(lay)

    def __added(self, filename: str):
        self.__musicPlayerWidget.setMedia(filename)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    player = MusicPlayerExample()
    player.show()
    sys.exit(app.exec_())
```

Result

![image](https://user-images.githubusercontent.com/55078043/159100272-0935aa46-598c-42b6-9c7f-4e1cf52d97f9.png)

