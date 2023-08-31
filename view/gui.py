from tkinter import *

from model import Model
from view.int_input import IntInput
from view.zoom_pan_canvas import ZoomPanCanvas


class GUI:
    POINT_RADIUS = 5
    STATION_RADIUS = 10
    ARROW_SHAPE = (16, 18, 5)
    COLORS = ["red", "green", "cyan", "orange", "green1", "orchid"]

    def __init__(self, model: Model):
        self.model = model
        tk = Tk()
        tk.title("Test")
        self.canvas = ZoomPanCanvas(tk, bg="white")
        self.canvas.pack(side="left", expand=True, fill="both")
        self.show_paths = BooleanVar(value=True)

        control_panel = Frame(tk)
        control_panel.pack(side="right", padx=10, pady=10, fill="y")
        self.result_info = Label(control_panel)
        self.delivery_count_input = IntInput(control_panel, "Delivery count:", 1, 999, 5)
        self.drones_count_input = IntInput(control_panel, "Drones count:", 1, 99, 3)
        self.test = IntInput(control_panel, "Test:")

        for widget in [
            self.result_info,
            self.delivery_count_input,
            self.drones_count_input,
            Checkbutton(control_panel, text="Show paths", variable=self.show_paths,
                        command=self.update_canvas),
            Button(control_panel, text="Refresh paths", command=self.refresh_paths, width=10),
            Button(control_panel, text="Restart", command=self.restart, width=10),
            Button(control_panel, text="Recenter", command=self.canvas.recenter, width=10)
        ]:
            widget.pack(pady=10)

        self.restart()
        tk.mainloop()

    def restart(self):
        self.model.generate_targets(self.delivery_count_input.get_value())
        self.refresh_paths()

    def refresh_paths(self):
        self.model.generate_paths(self.drones_count_input.get_value())
        self.update_canvas()

    def update_canvas(self):
        self.canvas.recenter()
        self.canvas.delete("all")
        self.draw_paths()
        self.draw_station()
        self.draw_delivery_points()
        self.result_info.config(text=self.get_result_info_text())

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
            self.draw_point(delivery.start, self.POINT_RADIUS, "white", index + 1)
            self.draw_point(delivery.end, self.POINT_RADIUS, "black", index + 1)

    def draw_point(self, point, radius, color="white", text=""):
        self.canvas.create_oval(point.x - radius, point.y - radius, point.x + radius, point.y + radius, fill=color)
        self.canvas.create_text(point.x, point.y - 2 * radius, text=text)

    def get_result_info_text(self):
        return (
            f"Distance: {round(self.model.best_distance, 2)}\n\n"
            f"Time: {round(self.model.best_time, 2)}\n\n"
            f"Drones: {sum(1 for path in self.model.paths if path)}/{len(self.model.paths)}"
        )
