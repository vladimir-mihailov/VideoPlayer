import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, window , video_source):
        self.window = window
        self.video_cource = video_source
        self. vid = cv2.VideoCapture(video_source)

        self. label = Label(window)
        self.label.pack()

        self.update()

        self.window.protocol("WM_DELITE_WINDOW", self.on_closing)

        self.window.mainloop()

    def update(self):
        ret, flame = self.vid.read()
        if ret:
            flame = cv2.cvtColor(flame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(flame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.window.after(20, self.update)


    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
            self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Видеоплеер")
    video_path = "your_video_file.mp4"

    player = VideoPlayer(root, video_path)
