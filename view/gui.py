import colorsys
from tkinter import ttk, filedialog

from controller import Controller
from model import Model
from view.tabs import OptimizationTab, EnvironmentTab, ViewTab
from view.zoom_pan_canvas import ZoomPanCanvas


class GUI:
    POINT_RADIUS = 7
    DEPOT_RADIUS = 8
    ARROW_SHAPE = (16, 18, 5)

    def __init__(self, model: Model, controller: Controller, root):
        self.model = model
        self.controller = controller

        root.title("VRP Optimization")
        self.canvas = ZoomPanCanvas(root, bg="white")
        self.canvas.pack(side="left", expand=True, fill="both")

        tabs = ttk.Notebook(root)
        tabs.pack(side="right", fill="y")

        self.optimization_tab = OptimizationTab(tabs, controller, pady=20)
        self.environment_tab = EnvironmentTab(tabs, controller, pady=20)
        self.view_tab = ViewTab(tabs, controller, pady=20)

        tabs.add(self.optimization_tab, text="Optimization")
        tabs.add(self.environment_tab, text="Environment")
        tabs.add(self.view_tab, text="View")

    def update_canvas(self):
        self.canvas.delete("all")
        self.draw_routes()
        self.draw_depot()
        self.draw_customer_points()
        self.optimization_tab.update_result(self.model)
        self.canvas.recenter()

    def draw_routes(self):
        if self.model.result:
            colors = self.generate_colors(len(self.model.result.routes))
            for index, route in enumerate(self.model.result.routes):
                for vector in route:
                    self.draw_vector(vector[0], vector[1], colors[index])

    def draw_vector(self, start, end, color="grey80"):
        if self.view_tab.should_show_routes():
            self.canvas.create_line(start.x, start.y, end.x, end.y, fill=color, arrow='last',
                                    arrowshape=self.ARROW_SHAPE)

    def draw_depot(self):
        self.draw_point(self.model.depot, radius=self.DEPOT_RADIUS, color="grey")

    def draw_customer_points(self):
        for index, customer in enumerate(self.model.customers):
            self.draw_point(customer, self.POINT_RADIUS, "white", index + 1)
            if hasattr(customer, "end"):
                self.draw_point(customer.end, self.POINT_RADIUS, "black", index + 1, "white")

    def draw_point(self, point, radius, color="white", text="", text_color="black"):
        self.canvas.create_oval(point.x - radius, point.y - radius, point.x + radius, point.y + radius,
                                outline="gray", fill=color, tags="fixed_scale")
        self.canvas.create_text(point.x, point.y, text=text, fill=text_color)

    @staticmethod
    def ask_open_file_dialog():
        return filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    @staticmethod
    def ask_save_as_file_dialog():
        return filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    @staticmethod
    def generate_colors(count):
        colors = []
        for i in range(count):
            hue = (i / count) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            colors.append(f'#{r:02X}{g:02X}{b:02X}')

        return colors
