from tkinter import *

from constants import *
from model import Model


class GUI:
    POINT_RADIUS = 5
    STATION_RADIUS = 10
    ARROW_SHAPE = (16, 18, 5)
    COLORS = ["red", "green", "cyan", "orange", "green1", "orchid"]

    def __init__(self, model: Model):
        self.model = model
        tk = Tk()
        tk.title("Test")

        self.canvas = Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack()

        generate_button = Button(tk, text="Restart", command=self.restart)
        generate_button.pack()

        self.show_paths = BooleanVar(value=True)
        show_paths_checkbox = Checkbutton(tk, text="Show paths", variable=self.show_paths, command=self.update_canvas)
        show_paths_checkbox.pack()

        self.restart()
        tk.mainloop()

    def restart(self):
        self.model.generate_targets()
        self.model.generate_paths()
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.draw_paths()
        self.draw_station()
        self.draw_delivery_points()

    def draw_paths(self):
        for index, path in enumerate(self.model.paths):
            for vector in path:
                self.draw_vector(vector[0], vector[1], self.COLORS[index % len(self.COLORS)])

    def draw_vector(self, start, end, color="grey80"):
        if self.show_paths.get():
            self.canvas.create_line(start.x, start.y, end.x, end.y, fill=color, arrow='last',
                                    arrowshape=self.ARROW_SHAPE)

    def draw_station(self):
        self.draw_point(self.model.station, radius=self.STATION_RADIUS, color="grey")

    def draw_delivery_points(self):
        for index, delivery in enumerate(self.model.delivery_requests):
            self.draw_point(delivery.start, self.POINT_RADIUS, "white", index)
            self.draw_point(delivery.end, self.POINT_RADIUS, "black", index)

    def draw_point(self, point, radius, color="white", text=""):
        self.canvas.create_oval(point.x - radius, point.y - radius, point.x + radius, point.y + radius, fill=color)
        self.canvas.create_text(point.x, point.y - 2 * radius, text=text)
