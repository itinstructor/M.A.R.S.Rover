#!/usr/bin/env python3
"""
    Name: video_stream_tkinter.py
    Author: William A Loring
    Created: 08/01/23
    Purpose: Stream video to a Tkinter interface using opencv
"""
# Raspberry Pi/Linux
# sudo pip3 install opencv-python
# sudo pip3 install pillow -U
# sudo apt-get install libatlas-base-dev
# sudo pip3 install numpy -U

# Windows
# sudo pip3 install opencv-python
# sudo pip3 install pillow -U
# sudo pip3 install numpy -U
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import cv2
# For image file time stamp
import time


class VideoStar():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Video Star OpenCV")
        # Set window location at 400x50
        self.root.geometry("+400+50")
        # Call self.quit when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.create_widgets()
        # Create VideoCapture object 0 = 1st camera
        self.cam = cv2.VideoCapture(0)
        # Start streaming to false
        self.streaming = False
        self.root.mainloop()

# ----------------------- START STOP VIDEO STREAM -------------------------#
    def start_stop_stream(self):
        if not self.streaming:
            self.start_stream()
        else:
            self.stop_stream()

# ------------------------ STOP VIDEO STREAM ------------------------------#
    def stop_stream(self):
        """Stop video capture"""
        self.streaming = False
        self.btn_start_stop.configure(text="Start Stream")
        # Release the camera capture object
        if self.cam.isOpened():
            self.cam.release()
        self.lbl_status_bar.configure(text=" Video Stream Stopped")

# ----------------------- START VIDEO CAPTURE -----------------------------#
    def start_stream(self):
        """Start video capture"""
        self.streaming = True
        self.lbl_status_bar.configure(text=" Video Stream Starting Up . . .")
        self.lbl_status_bar.update()
        self.btn_start_stop.configure(text="Stop Stream")
        self.lbl_status_bar.configure(text=" Video Stream Running . . .")
        self.update_stream()

# ------------------------ UPDATE STREAM ----------------------------------#
    def update_stream(self):
        if self.streaming:
            # Read camera image frame by frame
            # ret: Is a frame available True
            # frame: captured image
            ret, frame = self.cam.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.stream = photo
            else:
                self.lbl_status_bar.configure(text=" Failed to grab frame")
                # # Convert cv2 colorspace BGR to RGB
                # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                # # self.display_fps()
        # Update video stream every 10 ms when the main program isn't busy
        self.root.after(10, self.update_stream)

# ---------------------- TAKE SNAPSHOT ------------------------------------#
    def snapshot(self):
        """Get and write a single video frame to a jpg image"""
        # Get a frame from the video source
        ret, frame = self.get_frame()
        if ret == True:
            # Write video frame to jpg image with a date stamp
            cv2.imwrite(
                "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") +
                ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

# ---------------------- GET FRAME ----------------------------------------#
    def get_frame(self):
        """Get single frame from video stream"""
        # Set ret variable to false in case the camera is not open
        ret = False
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                # Return a boolean success flag
                # and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            self.lbl_status_bar.configure(
                text=" Video Capture must be started to capture a snapshot"
            )
            return (ret, None)

# ------------------ CREATE WIDGETS ---------------------------------------#
    def create_widgets(self):
        """Create widgets"""
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        message = f" OpenCV Video Stream"
        self.lbl_status_bar = tk.Label(
            self.root, text=message, anchor=tk.W, relief=tk.RIDGE)

        BUTTON_WIDTH = 16
        self.btn_start_stop = ttk.Button(
            self.root, text="Start Stream",
            command=self.start_stop_stream,
            width=BUTTON_WIDTH
        )
        self.btn_snapshot = ttk.Button(
            self.root, text="Snapshot",
            command=self.snapshot, width=BUTTON_WIDTH
        )
        self.btn_quit = ttk.Button(
            self.root, text="Quit", command=self.quit, width=BUTTON_WIDTH)

        self.canvas.grid(row=0, column=0, columnspan=4)

        self.btn_start_stop.grid(row=1, column=0)
        self.btn_snapshot.grid(row=1, column=1)
        self.btn_quit.grid(row=1, column=2)

        self.lbl_status_bar.grid(row=2, column=0, columnspan=4, sticky="WE")

        # Set padding for all widgets
        for child in self.root.winfo_children():
            child.grid_configure(padx=6, pady=6, ipadx=1, ipady=1)

# --------------------------- DISPLAY FPS ---------------------------------#
    def display_fps(self):
        """Get and display FPS"""
        # Get frames per second from cam capture properties
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)
        message = f"FPS: {self.fps}"
        self.lbl_status_bar.configure(text=message)
        self.lbl_status_bar.update()

# --------------------------- QUIT PROGRAM --------------------------------#
    def quit(self):
        try:
            # If cam is in use, release it
            if self.cam.isOpened():
                self.cam.release()
        except:
            pass
        self.root.destroy()


video_star = VideoStar()
