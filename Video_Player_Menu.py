import cv2
import tkinter as tk
from tkinter import Label, Button, Scale, filedialog, HORIZONTAL, messagebox, Menu
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer
import os

class VideoPlayer:
    def __init__(self, win):
        self.win = win
        self.win.geometry('800x600')
        self.win.title("Видеоплеер")

        self.video_source = None
        self.vid = None
        self.video_length = 0
        self.current_flame = 0

        self.create_menu()

        self.label = Label(win)
        self.label.pack()

        self.scale = Scale(win, from_=0, to=100,
                           orient=HORIZONTAL, label="Позиция",
                           command=self.scrub_video)
        self.scale.pack(fill= "x", pady= 10)

        self.volime_scale = Scale(win, from_=0, to=100,
                                  label="Громкость",
                                  command=self.change_volime)
        self.volime_scale.set(20)
        self.win.protocol("WM_DELITE_WIN", self.on_closing)

    def create_menu(self):
        menubar = Menu(self.win)
        self.win.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть видео",
                              command=self.select_video)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.win.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

    def select_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Vide Files",
                                                            "*.mp4; *.avi; *.mov; *.mkv")])
        if video_path and os.path.exists(video_path):
            self.start_video(video_path)
        else:
            messagebox.showerror("Ошибка", "Файл не найден или не выбран.")

    def start_video(self, video_path):
        if self.vid is not None and self.vid.isOpened():
            self.vid.release()
        if self.player is not None:
            self.player.close_player()

        self.video_source = video_path
        self.vid = cv2.VideoCapture(self.video_source)
        self.player = MediaPlayer(self.video_source)

        self.video_length = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.scale.config(to=self.video_length)

        self. player.set_volume(float(value)/100)

    def change_volime(self, value):
        if self.player:
            self.player.set_volume(float(value)/100)

    def scrub_video(self, value):
        if self.vid is not None and self.vid.isOpened():
            frame_pos = int(float(value))
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            self.current_flame = frame_pos

    def update(self):
        if self.vid is not None and self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.stvColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)

                audio_frame, val = self.label.get_frame()
                if val != 'eof' and audio_frame is not None:
                    pass

            self.win.after(30, update)
        else:
            self.win.after(30, update)


    def on_closing(self):
        if self.vid is not None and self.vid.isOpened():
            self.vid.release()
        if self.player is not None:
            self.player.close_player()
        self.win.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()

