import tkinter as tk


class IntInput(tk.Frame):
    MIN_ENTRY_WIDTH = 5

    def __init__(self, master, label="", min_value=None, max_value=None, default_value=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.label = tk.Label(self, text=label)
        self.label.pack(side="left")

        self.int_var = tk.StringVar(value=default_value)
        self.entry = tk.Entry(self, textvariable=self.int_var)
        self.entry.pack(side="left")

        self.min_value = min_value
        self.max_value = max_value

        vcmd = (self.register(self.validate_input), "%P")
        self.entry.config(validate="key", validatecommand=vcmd)

        self.update_entry_width()

    def validate_input(self, new_value):
        if new_value == "":
            return True
        try:
            int_value = int(new_value)
            return ((self.min_value is None or int_value >= self.min_value) and
                    (self.max_value is None or int_value <= self.max_value))
        except ValueError:
            return False

    def update_entry_width(self):
        max_value_length = len(str(self.max_value)) if self.max_value else self.MIN_ENTRY_WIDTH
        min_value_length = len(str(self.min_value)) if self.min_value else self.MIN_ENTRY_WIDTH
        self.entry.config(width=max(max_value_length, min_value_length))

    def get_value(self):
        return int(self.int_var.get()) if self.int_var.get() else 0
