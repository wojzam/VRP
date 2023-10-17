import colorsys
import tkinter as tk
from tkinter import ttk, filedialog

from model import Model
from view.tabs import OptimizationTab, EnvironmentTab, ViewTab
from view.zoom_pan_canvas import ZoomPanCanvas


class GUI:
    POINT_RADIUS = 7
    DEPOT_RADIUS = 8
    ARROW_SHAPE = (16, 18, 5)

    def __init__(self, model: Model):
        self.model = model
        root = tk.Tk()
        root.title("Delivery Route Optimization")
        self.canvas = ZoomPanCanvas(root, bg="white")
        self.canvas.pack(side="left", expand=True, fill="both")

        tabs = ttk.Notebook(root)
        tabs.pack(side="right", fill="y")

        self.optimization_tab = OptimizationTab(tabs, self.generate_routes, pady=20)
        self.environment_tab = EnvironmentTab(tabs, self.save_customers, self.read_customers, self.generate_customers,
                                              self.update_depot_position, pady=20)
        self.view_tab = ViewTab(tabs, self.update_canvas, self.canvas.recenter, pady=20)

        tabs.add(self.optimization_tab, text="Optimization")
        tabs.add(self.environment_tab, text="Environment")
        tabs.add(self.view_tab, text="View")

        self.generate_customers()
        self.generate_routes()
        root.mainloop()

    def generate_customers(self):
        self.model.generate_customers(self.environment_tab.get_customers_count(),
                                      self.environment_tab.get_customer_class())
        self.update_canvas()

    def generate_routes(self):
        self.model.generate_routes(
            self.optimization_tab.get_vehicles_count(),
            self.optimization_tab.get_size(),
            self.optimization_tab.get_generations_count(),
            self.optimization_tab.get_pc(),
            self.optimization_tab.get_pm(),
            self.optimization_tab.get_distance_factor(),
            self.optimization_tab.get_time_factor()
        )
        self.update_canvas()

    def update_depot_position(self):
        self.model.set_depot_position(*self.environment_tab.get_depot_position())
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.draw_routes()
        self.draw_depot()
        self.draw_customer_points()
        self.optimization_tab.update_result_info(self.model)
        self.canvas.recenter()

    def draw_routes(self):
        colors = self.generate_colors(len(self.model.routes))
        for index, route in enumerate(self.model.routes):
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

    def read_customers(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.model.read_customers(file_path)
            self.update_canvas()

    def save_customers(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.model.save_customers(file_path)

    @staticmethod
    def generate_colors(count):
        colors = []
        for i in range(count):
            hue = (i / count) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            colors.append(f'#{r:02X}{g:02X}{b:02X}')

        return colors
