from tkinter import Canvas

from constants import *


class ZoomPanCanvas(Canvas):
    def __init__(self, master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, *args, **kwargs):
        super().__init__(master, *args, **kwargs, width=width, height=height)

        self.current_scale = 1.0
        self.origin = (self.xview()[0], self.yview()[0])

        self.bind("<MouseWheel>", self.zoom)
        self.bind("<ButtonPress-1>", self.start_pan)
        self.bind("<B1-Motion>", self.pan)
        self.recenter()

    def zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.scale("all", CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, scale_factor, scale_factor)
        self.current_scale *= scale_factor

    def start_pan(self, event):
        self.scan_mark(event.x, event.y)

    def pan(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def recenter(self):
        self.xview_moveto(self.origin[0])
        self.yview_moveto(self.origin[1])
        self.scale("all", CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, 1 / self.current_scale, 1 / self.current_scale)
        self.current_scale = 1.0
