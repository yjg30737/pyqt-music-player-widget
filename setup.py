from setuptools import setup, find_packages

setup(
    name='pyqt-music-player-widget',
    version='0.3.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt music player widget',
    package_data={'pyqt_music_player_widget.ico': ['pause.svg', 'play.svg', 'stop.svg']},
    url='https://github.com/yjg30737/pyqt-music-player-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'mutagen>=1.45.1',
        'pyqt-media-slider>=0.0.1',
        'pyqt-svg-button>=0.0.1'
    ]
)