import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, window, video_source):
        self.window = window
        self.video_source = video_source
        self.vid = cv2.VideoCapture(video_source)

        self.label = Label(window)
        self.label.pack()

        self.update()  # Call to update method to start video playback
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)  # Corrected method name for closing
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk  # Store reference to avoid garbage collection
            self.label.configure(image=imgtk)  # Update label with new image
        self.window.after(20, self.update)  # Schedule the next update

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()  # Release the video capture
        self.window.destroy()  # Close the window

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Видеопроигрыватель")
    video_path = "your_video_file.mp4"  # Replace with your actual video file
    player = VideoPlayer(root, video_path)