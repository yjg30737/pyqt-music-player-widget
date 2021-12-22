from setuptools import setup, find_packages

setup(
    name='pyqt-music-player-widget',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt music player widget',
    package_data={'pyqt_music_player_widget.style': ['button.css'],
                  'pyqt_music_player_widget.ico': ['pause.png', 'play.png', 'stop.png']},
    url='https://github.com/yjg30737/pyqt-music-player-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-music-slider @ git+https://git@github.com/yjg30737/pyqt-music-slider.git@main'
    ]
)