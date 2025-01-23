
import cv2
import tkinter as tk
from tkinter import Label, Button, filedialog
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, window, video_source):
        self.window = window
        self.window.geometry("800x600")  # Увеличьте размер окна для видео
        self.video_source = video_source
        self.vid = cv2.VideoCapture(video_source)

        self.label = Label(window)
        self.label.pack()

        self.btn_select_video = Button(window, text='Выбрать видео', command=self.select_video)
        self.btn_select_video.pack()

        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def select_video(self):
        video_path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4; *.avi; *.mov; *.mkv')])
        if video_path:  # Уберите вызов видеопотока здесь
            self.video_source = video_path
            if self.vid.isOpened():  # Проверяем, открыт ли видеопоток
                self.vid.release()
            self.vid = cv2.VideoCapture(self.video_source)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.window.after(30, self.update)  # Уменьшено количество миллисекунд для более плавного воспроизведения

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()  # Исправлено на destroy()

if __name__ == '__main__':  # Исправлено на правильную конструкцию
    root = tk.Tk()
    root.title("Видеоплеер")
    video_path = "your_video_file.mp4"

    player = VideoPlayer(root, video_path)

