from tkinter import Button, Checkbutton, Frame, Label, BooleanVar
from tkinter import ttk

from customer import Customer
from customer_pair import CustomerPair
from model import Model
from view.input import IntInput, FloatInput


class OptimizationTab(Frame):
    def __init__(self, master, generate_routes, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._vehicles_count_input = IntInput(self, "Vehicles:", 0, 99, Model.DEFAULT_VEHICLES_COUNT)
        row1_frame, row2_frame = Frame(self), Frame(self)
        self._size_input = IntInput(row1_frame, "Population:", 0, 999, Model.DEFAULT_POP_SIZE)
        self._pc_input = FloatInput(row1_frame, "PC:", 0., 1., Model.DEFAULT_PC, width=4)
        self._generations_input = IntInput(row2_frame, "Generations:", 0, 999, Model.DEFAULT_GENERATIONS)
        self._pm_input = FloatInput(row2_frame, "PM:", 0., 1., Model.DEFAULT_PM, width=4)
        Button(self, text="Run", command=generate_routes)
        self._result_info = Label(ttk.LabelFrame(self, text="Result"), justify="left")

        pack_children_of(self)
        self._size_input.pack(side="left")
        self._pc_input.pack(side="right")
        self._generations_input.pack(side="left")
        self._pm_input.pack(side="right")
        self._result_info.pack(pady=10)

    def update_result_info(self, model: Model):
        self._result_info.config(text=self.retrieve_result_info_text(model))

    def get_vehicles_count(self):
        return self._vehicles_count_input.get_value()

    def get_size(self):
        return self._size_input.get_value()

    def get_generations_count(self):
        return self._generations_input.get_value()

    def get_pc(self):
        return self._pc_input.get_value()

    def get_pm(self):
        return self._pm_input.get_value()

    @staticmethod
    def retrieve_result_info_text(model: Model):
        return (
            f"Distance: {round(model.best_distance, 2)}\n\n"
            f"Time: {round(model.best_time, 2)}\n\n"
            f"Score: {round(model.best_score, 2)}\n\n"
            f"Exec. time: {round(model.execution_time, 2)}s\n\n"
            f"Vehicles: {sum(1 for route in model.routes if route)}/{len(model.routes)}"
        )


class EnvironmentTab(Frame):
    ONE_TO_ALL = "one to all"
    ONE_TO_ONE = "one to one"
    DELIVERY_TYPE_TO_CUSTOMER = {ONE_TO_ALL: Customer, ONE_TO_ONE: CustomerPair}

    def __init__(self, master, save_file, read_file, generate_targets, update_depot_position, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        customers_file_frame = ttk.LabelFrame(self, text="Customers file")
        read_button = Button(customers_file_frame, command=read_file, text="Read", width=10)
        save_button = Button(customers_file_frame, command=save_file, text="Save", width=10)
        depot_position_frame = ttk.LabelFrame(self, text="Depot position")
        self._depot_x_input = IntInput(depot_position_frame, "x:", -9999, 9999, 0)
        self._depot_y_input = IntInput(depot_position_frame, "y:", -9999, 9999, 0)
        Button(depot_position_frame, text="Update", command=update_depot_position)
        self._delivery_type = ttk.Combobox(self, state="readonly", values=[self.ONE_TO_ALL, self.ONE_TO_ONE])
        self._delivery_type.set(self.ONE_TO_ALL)
        self._customer_count_input = IntInput(self, "Customers:", 0, 999, Model.DEFAULT_CUSTOMERS_COUNT)
        Button(self, text="Generate", command=generate_targets)

        pack_children_of(self)
        pack_children_of(depot_position_frame, padx=5, pady=5, side="left")
        read_button.pack(padx=5, pady=5, side="left")
        save_button.pack(padx=5, pady=5, side="right")

    def get_depot_position(self):
        return self._depot_x_input.get_value(), self._depot_y_input.get_value()

    def get_customer_class(self):
        return self.DELIVERY_TYPE_TO_CUSTOMER[self._delivery_type.get()]

    def get_customers_count(self):
        return self._customer_count_input.get_value()


class ViewTab(Frame):
    def __init__(self, master, update_canvas, recenter, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._show_routes = BooleanVar(value=True)
        Checkbutton(self, text="Show routes", variable=self._show_routes, command=update_canvas)
        Button(self, text="Recenter", command=recenter)

        pack_children_of(self)

    def should_show_routes(self):
        return self._show_routes.get()


def pack_children_of(root, padx=20, pady=10, fill="x", **kwargs):
    for c in root.children:
        root.children[c].pack(padx=padx, pady=pady, fill=fill, **kwargs)
