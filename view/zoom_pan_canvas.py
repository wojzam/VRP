from tkinter import Canvas

from constants import *


class ZoomPanCanvas(Canvas):
    def __init__(self, master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, *args, **kwargs):
        super().__init__(master, *args, **kwargs, width=width, height=height)

        self.current_scale = 1.0

        self.bind("<MouseWheel>", self.zoom)
        self.bind("<ButtonPress-1>", self.start_pan)
        self.bind("<B1-Motion>", self.pan)

    def zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self._update_scale(scale_factor)

    def start_pan(self, event):
        self.scan_mark(event.x, event.y)

    def pan(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    def recenter(self):
        self._reset_view()
        width, height = self.winfo_width(), self.winfo_height()
        self._resize_to_fit(width, height)
        self._center_view(width, height)

    def _reset_view(self):
        self.xview_moveto(0)
        self.yview_moveto(0)
        self._update_scale(1 / self.current_scale)
        self.current_scale = 1.0
        self.update()

    def _center_view(self, width, height):
        bbox = self.bbox("all")
        self.scan_mark(0, 0)
        self.scan_dragto((width - (bbox[0] + bbox[2])) // 2, (height - (bbox[1] + bbox[3])) // 2, gain=1)

    def _resize_to_fit(self, width, height):
        bbox = self.bbox("all")
        scale_factor = min(width / (bbox[2] - bbox[0] + 2 * CANVAS_MARGIN),
                           height / (bbox[3] - bbox[1] + 2 * CANVAS_MARGIN))
        self._update_scale(scale_factor)

    def _update_scale(self, scale_factor):
        self.scale("all", 0, 0, scale_factor, scale_factor)
        self.current_scale *= scale_factor
        self._maintain_fixed_size(scale_factor)

    def _maintain_fixed_size(self, scale_factor):
        fixed_scale_items = self.find_withtag("fixed_scale")
        for item in fixed_scale_items:
            x1, y1, x2, y2 = self.coords(item)
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            scaled_center_x = center_x * scale_factor
            scaled_center_y = center_y * scale_factor
            self.move(item, scaled_center_x - center_x, scaled_center_y - center_y)
            self.scale(item, 0, 0, 1 / scale_factor, 1 / scale_factor)

    def delete(self, *args):
        super().delete(*args)
        self._reset_view()
