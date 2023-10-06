from tkinter import *
from tkinter import ttk

from customer_pair import CustomerPair
from model import Model
from view.int_input import IntInput
from view.zoom_pan_canvas import ZoomPanCanvas


class GUI:
    POINT_RADIUS = 4
    DEPOT_RADIUS = 8
    ARROW_SHAPE = (16, 18, 5)
    COLORS = ["red", "green", "cyan", "orange", "green1", "orchid"]
    ONE_TO_ALL_NAME = "one to all"
    ONE_TO_ONE_NAME = "one to one"

    def __init__(self, model: Model):
        self.model = model
        tk = Tk()
        tk.title("Delivery Route Optimization")
        self.canvas = ZoomPanCanvas(tk, bg="white")
        self.canvas.pack(side="left", expand=True, fill="both")
        self.show_routes = BooleanVar(value=True)

        control_panel = Frame(tk)
        control_panel.pack(side="right", padx=10, pady=10, fill="y")
        self.result_info = Label(control_panel)
        self.customer_count_input = IntInput(control_panel, "Customers:", 0, 999, Model.DEFAULT_CUSTOMERS_COUNT)
        self.vehicles_count_input = IntInput(control_panel, "Vehicles:", 0, 99, Model.DEFAULT_VEHICLES_COUNT)
        self.size_input = IntInput(control_panel, "Population:", 0, 999, Model.DEFAULT_POP_SIZE)
        self.generations_input = IntInput(control_panel, "Generations:", 0, 999, Model.DEFAULT_GENERATIONS)
        self.delivery_type = ttk.Combobox(control_panel, state="readonly", width=10,
                                          values=[self.ONE_TO_ALL_NAME, self.ONE_TO_ONE_NAME])
        self.delivery_type.set(self.ONE_TO_ALL_NAME)

        for widget in [
            self.delivery_type,
            self.customer_count_input,
            Button(control_panel, text="Generate", command=self.generate_targets, width=10),
            self.vehicles_count_input,
            self.size_input,
            self.generations_input,
            Button(control_panel, text="Run", command=self.generate_routes, width=10),
            self.result_info,
            Checkbutton(control_panel, text="Show routes", variable=self.show_routes, command=self.update_canvas),
            Button(control_panel, text="Recenter", command=self.canvas.recenter, width=10)
        ]:
            widget.pack(pady=10)

        self.generate_targets()
        self.generate_routes()
        tk.mainloop()

    def generate_targets(self):
        if self.delivery_type.get() == self.ONE_TO_ALL_NAME:
            self.model.generate_targets(self.customer_count_input.get_value())
        else:
            # TODO : GUI should not have knowledge about DeliveryRequest
            self.model.generate_targets(self.customer_count_input.get_value(), customer_type=CustomerPair)
        self.update_canvas()

    def generate_routes(self):
        self.model.generate_routes(
            self.vehicles_count_input.get_value(),
            self.size_input.get_value(),
            self.generations_input.get_value()
        )
        self.update_canvas()

    def update_canvas(self):
        self.canvas.recenter()
        self.canvas.delete("all")
        self.draw_routes()
        self.draw_depot()
        self.draw_customer_points()
        self.result_info.config(text=self.get_result_info_text())

    def draw_routes(self):
        for index, route in enumerate(self.model.routes):
            for vector in route:
                self.draw_vector(vector[0], vector[1], self.COLORS[index % len(self.COLORS)])

    def draw_vector(self, start, end, color="grey80"):
        if self.show_routes.get():
            self.canvas.create_line(start.x, start.y, end.x, end.y, fill=color, arrow='last',
                                    arrowshape=self.ARROW_SHAPE)

    def draw_depot(self):
        self.draw_point(self.model.depot, radius=self.DEPOT_RADIUS, color="grey")

    def draw_customer_points(self):
        for index, customer in enumerate(self.model.customers):
            self.draw_point(customer, self.POINT_RADIUS, "white", index + 1)
            if self.delivery_type.get() == self.ONE_TO_ONE_NAME:
                self.draw_point(customer.end, self.POINT_RADIUS, "black", index + 1)

    def draw_point(self, point, radius, color="white", text=""):
        self.canvas.create_oval(point.x - radius, point.y - radius, point.x + radius, point.y + radius, fill=color)
        self.canvas.create_text(point.x, point.y - 2 * radius, text=text)

    def get_result_info_text(self):
        return (
            f"Distance: {round(self.model.best_distance, 2)}\n\n"
            f"Time: {round(self.model.best_time, 2)}\n\n"
            f"Vehicles: {sum(1 for route in self.model.routes if route)}/{len(self.model.routes)}"
        )
