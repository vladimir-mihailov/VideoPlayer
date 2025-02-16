import sys
from PyQt5.QtWidgets import QApplication, QSlider, QAction,  QMainWindow, QWidget, QVBoxLayout,  QMenu, QFileDialog, QSlider, QAction
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
import vlc
from sympy.physics.units import speed


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
        self.video_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.video_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Создание меню
        self.create_menu()

        # Таймер для обновления позиции воспроизведения
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)

    def create_menu(self):
        # контекстноe меню
        self.context_menu = QMenu(self)

        # Пункты меню
        open_action = QAction("Открыть файл", self)
        open_action.triggered.connect(self.open_file)
        self.context_menu.addAction(open_action)

        save_action = QAction("Сохранит видео как", self)
        save_action.triggered.connect(self.save_video)
        self.context_menu.addAction(save_action)

        playback_menu = self.context_menu.addMenu("Настройки воспроизведения")
        speed_menu = playback_menu.addMenu("Скорость воспроизведения")
        speeds = [("0,5", 0.5), ("1x", 1.0), ("1,5", 1.5), ("2x", 2.0)]
        for text, speed in speeds:
            action = QAction(text, self)
            action.triggered.connect(lambda _, s=speed: self.set_playback_speed(s))
            speed_menu.addAction(action)

        loop_action = QAction("Циклическое воспроизведение", self)
        loop_action.setCheckable(True)
        loop_action.triggered.connect(self.toggle_loop)
        playback_menu.addAction(loop_action)

    def show_context_menu(self):
        #Отображение контекстного меню
        self.context_menu.exec_(self.video_widget.mapToGlobal(position))

    def open_file(self):
         # Открытие видеофайла
        file_name, _ = QFileDialog.getOpenFileNames(self, "Открыть видео", "", "Video Files "
                                                                               "(*.mp4 *.avi *.mkv *.mov *.wmv)")
        if file_name:
            media = self.instance.media_new(file_name)
            self.media_player.set_media(media)
            self.media_player.play()

    def save_video(self):
        # Сохранение видео (заглушка)
        print("Функция сохранения видео не реализована.")

    def set_playback_speed(self, speed):
       # Установка скорости воспроизведения
        self.media_player.set_rate(speed)

    def toggle_loop(self, checked):
       # Включение/выключение циклического воспроизведения
        (self. media_player.set_playback_mode
         (vlc.PlaybackMode.loop if checked else vlc.PlaybackMode.default))

    def update_ui(self):
        # Обновление интерфейса
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
