import cv2
import tkinter as tk
from tkinter import Label, Button, Scale, filedialog, HORIZONTAL, messagebox
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer
import os

class VideoPlayer:
    def __init__(self, window, video_source=None):
        self.window = window
        self.window.geometry("800x800")
        self.video_source = video_source
        self.vid = None
        self.player = None

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

        if self.video_source and os.path.exists(self.video_source):
            self.start_video(self.video_source)
        else:
            self.select_video()  # Prompt the user to select a video file

        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.mainloop()

    def start_video(self, video_path):
        """Initialize video playback with the given video path."""
        if self.vid is not None and self.vid.isOpened():
            self.vid.release()
        if self.player is not None:
            self.player.close_player()

        self.video_source = video_path
        self.vid = cv2.VideoCapture(self.video_source)
        self.player = MediaPlayer(self.video_source)  # Correct initialization
        self.player.set_volume(self.volime_scale.get() / 100)  # Set volume after initialization

    def select_video(self):
        """Open a file dialog to select a video file."""
        video_path = filedialog.askopenfilename(filetypes=[("Video Files",
                                                            "*.mp4; *.avi; *.mov; *.mkv")])
        if video_path and os.path.exists(video_path):
            self.start_video(video_path)
        else:
            messagebox.showerror("Ошибка", "Файл не найден или не выбран.")

    def change_volime(self, value):
        """Change the volume of the video player."""
        if self.player:
            self.player.set_volume(float(value) / 100)

    def update(self):
        """Update the video frame in the GUI."""
        if self.vid is not None and self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)

                audio_frame, val = self.player.get_frame()
                if val != 'eof' and audio_frame is not None:
                    pass
                self.window.after(30, self.update)
        else:
            self.window.after(30, self.update)

    def on_closing(self):
        """Handle window closing event."""
        if self.vid is not None and self.vid.isOpened():
            self.vid.release()
        if self.player is not None:
            self.player.close_player()
        self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Видеоплеер")
    player = VideoPlayer(root)






