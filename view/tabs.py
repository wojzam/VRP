from tkinter import Button, Checkbutton, Frame, Label, BooleanVar
from tkinter import ttk

from customer import Customer
from customer_pair import CustomerPair
from model import Model, Result
from view.input import IntInput, FloatInput


class OptimizationTab(Frame):
    def __init__(self, master, generate_routes, navigate_result_history, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._vehicles_count_input = IntInput(self, "Vehicles:", 0, 99, Model.DEFAULT_VEHICLES_COUNT)
        row1_frame, row2_frame, row3_frame = Frame(self), Frame(self), Frame(self)
        self._size_input = IntInput(row1_frame, "Population:", 0, 999, Model.DEFAULT_POP_SIZE)
        self._pc_input = FloatInput(row1_frame, "PC:", 0., 1., Model.DEFAULT_PC, width=4)
        self._generations_input = IntInput(row2_frame, "Generations:", 0, 999, Model.DEFAULT_GENERATIONS)
        self._pm_input = FloatInput(row2_frame, "PM:", 0., 1., Model.DEFAULT_PM, width=4)
        self._distance_factor_input = FloatInput(row3_frame, "score = distance*", -999., 999.,
                                                 Model.DEFAULT_DISTANCE_FACTOR, width=4)
        self._time_factor_input = FloatInput(row3_frame, "+ time*", -999., 999., Model.DEFAULT_TIME_FACTOR, width=4)
        Button(self, text="Run", command=generate_routes)
        self.result_frame = ttk.LabelFrame(self, text="Result")
        self._result_info = Label(self.result_frame, justify="left")
        navigation_frame = Frame(self.result_frame)
        Button(navigation_frame, text="⬅", command=navigate_result_history(-1))
        self.pagination_indicator = Label(navigation_frame, text="")
        Button(navigation_frame, text="➡", command=navigate_result_history(1))

        pack_children_of(self)
        pack_children_of(row3_frame, padx=0, pady=0, side="left")
        pack_children_of(self.result_frame, pady=10)
        pack_children_of(navigation_frame, padx=5, pady=0, side="left", expand=True)
        self._size_input.pack(side="left")
        self._pc_input.pack(side="right")
        self._generations_input.pack(side="left")
        self._pm_input.pack(side="right")

    def update_result(self, model: Model):
        if not model.result:
            self.result_frame.pack_forget()
        else:
            self.result_frame.pack(padx=20, pady=10, fill="x")
            self._result_info.config(text=self.retrieve_result_info_text(model.result))
            self.pagination_indicator.config(text=model.get_pagination_indicator())

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

    def get_distance_factor(self):
        return self._distance_factor_input.get_value()

    def get_time_factor(self):
        return self._time_factor_input.get_value()

    @staticmethod
    def retrieve_result_info_text(result: Result):
        return (
            f"Distance: {round(result.distance, 2)}\n\n"
            f"Time: {round(result.time, 2)}\n\n"
            f"Score: {round(result.score, 2)}\n\n"
            f"Exec. time: {round(result.execution_time, 2)}s\n\n"
            f"Vehicles: {sum(1 for route in result.routes if route)}/{len(result.routes)}"
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
