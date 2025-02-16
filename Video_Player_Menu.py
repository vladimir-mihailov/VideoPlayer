import sys
from PyQt5.QtWidgets import QApplication, QSlider, QAction,  QMainWindow, QWidget, QVBoxLayout,  QMenu, QFileDialog, QSlider, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
import vlc

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Видеоплеер")
        self.setGeometry(100, 100, 800, 600)

        # Создание VLC-плеера
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        # Виджет для отображения видео
        self.video_widget = QWidget(self)
        self.setCentralWidget(self.video_widget)

        # Установка виджета для VLC
        if sys.platform == "win32":
            self.media_player.set_hwnd(self.video_widget.winId())
        else:
            self.media_player.set_xwindow(self.video_widget.winId())

        # Создание контекстного меню
