import codecs
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='pyqt-music-player-widget',
    version='0.0.31',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt music player widget',
    package_data={'pyqt_music_player_widget.ico': ['pause.svg', 'play.svg', 'stop.svg', 'volume.svg', 'mute.svg']},
    url='https://github.com/nikonru/pyqt-music-player-widget.git',
    long_description_content_type='text/markdown',
    long_description=long_description,
    install_requires=[
        'PyQt5>=5.8',
        'audioread>=3.0.1',
        'pyqt-media-slider>=0.0.1',
        'pyqt-svg-button>=0.0.1'
    ]
)
