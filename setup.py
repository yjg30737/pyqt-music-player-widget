from setuptools import setup, find_packages

setup(
    name='pyqt-music-player-widget',
    version='0.2.0',
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
        'pyqt-music-slider @ git+https://git@github.com/yjg30737/pyqt-music-slider.git@main',
        'pyqt-svg-icon-pushbutton @ git+https://git@github.com/yjg30737/pyqt-svg-icon-pushbutton.git@main'
    ]
)