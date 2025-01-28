import cv2
import tkinter as tk
from tkinter import Label, Button, Scale, filedialog, HORIZONTAL
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer

class VideoPlayer:
    def __init__(self, window, video_source):
        self.window = window
        self. window.geometry("800x800")
        self.video_source = video_source
        self.vid = cv2.VideoCapture(video_source)
        self.player = MediaPlayer(video_source)

        self.label = Label(window)
        self.label.pack()

        self.btn_select_video = Button(window,
                                       text="Выбрать видео",
                                       command=self.select_video)
        self.btn_select_video.pack()

        self.volime_scale = Scale(window, from_=0, to=100,
                                  orient=HORIZONTAL, label="Громкость",
                                  command=self.change_volime)
        self.volime_scale.set(20)
        self.volime_scale.pack()

        self.update()
        self.window.protocol("WM_DELITE_WINDOW", self.on_closing)

        self.window.mainloop()

    def select_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Video Files",
                                                            "*.mp4; *.avi; *.mov; *.mkv")])
        if video_path:
            if self.vid.isOpened():
                self.vid.release()
            if self.player:
                self.player.close_player()
                self.video_source = video_path
                self.vid = cv2.VideoCapture(self.video_source)
                self.player = MediaPlayer(self.video_source)
                self.player.set_volume(self.volime_scale.get()/100)


    def change_volime(self, value):
        if self.player:
            self.player.set_volume(float(value)/100)

    def update(self):
        ret, flame = self.vid.read()
        if ret:
            flame = cv2.svtColor(flame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(flame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            audio_frame, val = self.player.get_frame()
            if val != 'eof'and audio_frame is not None:
                pass
            self.window.after(30, self.update)

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.player:
            self.player.close_player()
        self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Видеоплеер")
    video_path = "your_video_file.mp4"

player = VideoPlayer(root, video_path)







