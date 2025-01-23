
import cv2
import tkinter as tk
from tkinter import Label, Button, Scale, filedialog, HORIZONTAL
from pygame import mixer
from PIL import Image, ImageTk
import os

class VideoPlayer:
    def __init__(self, window, video_source):
        self.window = window
        self.window.geometry("800x600")
        self.video_source = video_source
        mixer.init()
        self.vid = cv2.VideoCapture(video_source)

        self.label = Label(window)
        self.label.pack()

        self.btn_select_video = Button(window, text='Выбрать видео', command=self.select_video)
        self.btn_select_video.pack()

        self.volume_scale = Scale(window, from_=0, to=100, orient=HORIZONTAL, label='Громкость', command=self.change_volume)
        self.volume_scale.set(20)
        self.volume_scale.pack()

        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def select_video(self):
        video_path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4; *.avi; *.mov; *.mkv')])
        if video_path:
            if self.vid.isOpened():
                self.vid.release()
                mixer.music.stop()  # Stop any currently playing music
            self.video_source = video_path
            self.vid = cv2.VideoCapture(self.video_source)

            # Load and play the audio of the video (if applicable)
            audio_path = os.path.splitext(video_path)[0] + '.mp3'  # Assuming audio is in mp3 format
            if os.path.exists(audio_path):
                mixer.music.load(audio_path)
            else:
                # If there is no separate audio, just play the video without audio
                mixer.music.load(self.video_source)
            mixer.music.play()

    def change_volume(self, volume):
        mixer.music.set_volume(int(volume) / 100)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        self.window.after(30, self.update)

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        mixer.music.stop()
        self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Видеоплеер")
    video_path = "your_video_file.mp4"  # Replace with your video file path
    player = VideoPlayer(root, video_path)



