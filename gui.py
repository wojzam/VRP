from tkinter import *

from constants import *
from model import Model

COLORS = ["red", "green", "cyan", "orange", "green1", "orchid"]


class GUI:

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
        self.model.generate_delivery_requests()
        self.model.generate_drones_tasks()
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.draw_station()
        self.draw_delivery_points()
        self.draw_all_drones_paths()

    def draw_station(self):
        self.canvas.create_oval(self.model.station.x - STATION_RADIUS,
                                self.model.station.y - STATION_RADIUS,
                                self.model.station.x + STATION_RADIUS,
                                self.model.station.y + STATION_RADIUS,
                                fill="grey")

    def draw_delivery_points(self):
        for index, delivery in enumerate(self.model.delivery_requests):
            self.draw_point(delivery.start, "white", index)
            self.draw_point(delivery.end, "black", index)
            self.draw_path(delivery.start, delivery.end)

    def draw_point(self, point, color="white", text=""):
        self.canvas.create_oval(point.x - POINT_RADIUS,
                                point.y - POINT_RADIUS,
                                point.x + POINT_RADIUS,
                                point.y + POINT_RADIUS,
                                fill=color)
        self.canvas.create_text(point.x, point.y - 2 * POINT_RADIUS, text=text)

    def draw_path(self, start, end, color="grey80"):
        if self.show_paths.get():
            self.canvas.create_line(start.x, start.y, end.x, end.y, fill=color, arrow='last', arrowshape=ARROW_SHAPE)

    def draw_all_drones_paths(self):
        for index, drone in enumerate(self.model.drones_tasks):
            self.draw_drone_paths(drone, COLORS[index % len(COLORS)])

    def draw_drone_paths(self, path, color):
        if path:
            self.draw_path(self.model.station, self.model.delivery_requests[path[0]].start, color)
        for i in range(len(path) - 1):
            self.draw_path(self.model.delivery_requests[path[i]].end,
                           self.model.delivery_requests[path[i + 1]].start,
                           color)
