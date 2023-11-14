import tkinter as tk

from model import Model


class Controller:
    def __init__(self, model: Model):
        self.root = tk.Tk()
        self.model = model
        from view import GUI
        self.view = GUI(model, self, self.root)

    def run(self):
        self.generate_customers()
        self.generate_routes()
        self.root.mainloop()

    def generate_customers(self, *args, **kwargs):
        self.model.generate_customers(*args, **kwargs)
        self.update_view()

    def generate_customers_along_the_lines(self, *args, **kwargs):
        self.model.generate_customers_along_the_lines(*args, **kwargs)
        self.update_view()

    def generate_routes(self, *args, **kwargs):
        self.model.generate_routes(*args, **kwargs)
        self.update_view()

    def navigate_result_history(self, index_change):
        def inner():
            self.model.result_history.navigate(index_change)
            self.update_view()

        return inner

    def update_depot_position(self, *args, **kwargs):
        self.model.set_depot_position(*args, **kwargs)
        self.update_view()

    def update_view(self):
        self.view.update_canvas()

    def recenter(self):
        self.view.canvas.recenter()

    def read_customers(self):
        file_path = self.view.ask_open_file_dialog()
        if file_path:
            self.model.read_customers(file_path)
            self.update_view()

    def save_customers(self):
        file_path = self.view.ask_save_as_file_dialog()
        if file_path:
            self.model.save_customers(file_path)
