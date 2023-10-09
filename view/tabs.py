from tkinter import Button, Checkbutton, Frame, Label, BooleanVar
from tkinter import ttk

from model import Model
from view.int_input import IntInput


class OptimizationTab(Frame):
    def __init__(self, master, generate_routes, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._vehicles_count_input = IntInput(self, "Vehicles:", 0, 99, Model.DEFAULT_VEHICLES_COUNT)
        self._size_input = IntInput(self, "Population:", 0, 999, Model.DEFAULT_POP_SIZE)
        self._generations_input = IntInput(self, "Generations:", 0, 999, Model.DEFAULT_GENERATIONS)
        Button(self, text="Run", command=generate_routes, width=10)
        self._result_info = Label(ttk.LabelFrame(self, text="Result"))

        pack_children_of(self)
        self._result_info.pack(pady=10)

    def update_result_info(self, model: Model):
        self._result_info.config(text=self.retrieve_result_info_text(model))

    def get_vehicles_count(self):
        return self._vehicles_count_input.get_value()

    def get_size(self):
        return self._size_input.get_value()

    def get_generations_count(self):
        return self._generations_input.get_value()

    @staticmethod
    def retrieve_result_info_text(model: Model):
        return (
            f"Distance: {round(model.best_distance, 2)}\n\n"
            f"Time: {round(model.best_time, 2)}\n\n"
            f"Vehicles: {sum(1 for route in model.routes if route)}/{len(model.routes)}"
        )


class EnvironmentTab(Frame):
    ONE_TO_ALL = "one to all"
    ONE_TO_ONE = "one to one"

    def __init__(self, master, generate_targets, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._delivery_type = ttk.Combobox(self, state="readonly", width=10, values=[self.ONE_TO_ALL, self.ONE_TO_ONE])
        self._delivery_type.set(self.ONE_TO_ALL)
        self._customer_count_input = IntInput(self, "Customers:", 0, 999, Model.DEFAULT_CUSTOMERS_COUNT)
        Button(self, text="Generate", command=generate_targets, width=10)

        pack_children_of(self)

    def get_delivery_type(self):
        return self._delivery_type.get()

    def get_customers_count(self):
        return self._customer_count_input.get_value()


class ViewTab(Frame):
    def __init__(self, master, update_canvas, recenter, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._show_routes = BooleanVar(value=True)
        Checkbutton(self, text="Show routes", variable=self._show_routes, command=update_canvas)
        Button(self, text="Recenter", command=recenter, width=10)

        pack_children_of(self)

    def should_show_routes(self):
        return self._show_routes.get()


def pack_children_of(root):
    for c in root.children:
        root.children[c].pack(pady=10)
