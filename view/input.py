import tkinter as tk


class FloatInput(tk.Frame):
    MIN_ENTRY_WIDTH = 5

    def __init__(self, master, label="", min_value=None, max_value=None, default_value=None, width=None, *args,
                 **kwargs):
        super().__init__(master, *args, **kwargs)

        self.label = tk.Label(self, text=label)
        self.label.pack(side="left")

        self.var = tk.StringVar(value=default_value)
        self.entry = tk.Entry(self, textvariable=self.var, width=width)
        self.entry.pack(side="left")

        self.min_value = min_value
        self.max_value = max_value

        vcmd = (self.register(self.validate_input), "%P")
        self.entry.config(validate="key", validatecommand=vcmd)

        if not width:
            self.update_entry_width()

    def validate_input(self, new_value):
        if new_value == "":
            return True
        try:
            value = self.convert_input(new_value)
            return ((self.min_value is None or value >= self.min_value) and
                    (self.max_value is None or value <= self.max_value))
        except ValueError:
            return False

    def update_entry_width(self):
        max_value_length = len(str(self.max_value)) if self.max_value is not None else self.MIN_ENTRY_WIDTH
        min_value_length = len(str(self.min_value)) if self.min_value is not None else self.MIN_ENTRY_WIDTH
        self.entry.config(width=max(max_value_length, min_value_length))

    def convert_input(self, value):
        return float(value) if value else 0.

    def get_value(self):
        return self.convert_input(self.var.get())


class IntInput(FloatInput):
    def convert_input(self, value):
        return int(value) if value else 0
