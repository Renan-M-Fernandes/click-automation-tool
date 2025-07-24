import tkinter as tk
from tkinter import messagebox, ttk
from styles import DARK_STYLE

class BaseScreen(tk.Frame):
    def __init__(self, parent, controller, config=None, loc_manager=None):
        super().__init__(parent, bg=DARK_STYLE["colors"]["bg_main"])
        self.controller = controller
        self.config_data = config or {}
        self.locale = loc_manager or {}

        # Make this frame fill the entire container cell
        self.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.center_frame = tk.Frame(self, bg=DARK_STYLE["colors"]["bg_main"])
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")  # <== Centers it

        # Inner frame for stacking widgets
        self.content = tk.Frame(self.center_frame, bg=DARK_STYLE["colors"]["bg_main"])
        self.content.pack()

        self.configure_widgets()

    def create_button(self, text, command=None):
        btn = tk.Button(
            self.content,
            text=text,
            command=command,
            **DARK_STYLE["button"],
            height= 1,
            width=12
        )
        btn.pack(pady=6)
        return btn

    def create_label(self, text, font="title"):
        lbl = tk.Label(
            self.content,
            text=text,
            **DARK_STYLE["label"],
        )
        lbl.pack(pady=6)
        return lbl

    def create_title_label(self, text, font="title"):
        lbl = tk.Label(
            self.content,
            text=text,
            **DARK_STYLE["title_label"],
        )
        lbl.pack(pady=6)
        return lbl

    def create_entry_num(self, default=0.0):
        def validate_float(value_if_allowed):
            if value_if_allowed == "":
                return True  # allow empty for editing
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False

        vcmd = self.content.register(validate_float)

        entr = tk.Entry(
            self.content,
            width=22,
            validate="key",
            validatecommand=(vcmd, "%P"),
        )
        entr.pack(pady=4, fill="x", padx=10)
        return entr

    def create_entry_alpha(self, default=0):
        entr = tk.Entry(
            self.content,
            width = 22
        )
        entr.pack(pady=4, fill="x", padx=10)
        return entr


    def create_combo_box(self, values, default_index=0):
        combo = ttk.Combobox(self.content, values=values, state="readonly")
        combo.current(default_index)
        combo.pack(pady=4, fill="x", padx=10)
        return combo


    def show_message_box(self, title, text):
        wnm = messagebox.showinfo(
            title=title,
            message=text,

        )
        return wnm

    def create_button_row(self, buttons):
        row_frame = tk.Frame(self.content, bg=DARK_STYLE["colors"]["bg_main"])
        row_frame.pack(pady=10, fill="x", padx=10)

        self.buttons = []  # Store references here

        for i, btn_info in enumerate(buttons):
            btn = tk.Button(
                row_frame,
                text=btn_info["text"],
                command=btn_info["command"],
                width=btn_info.get("width", 12),
                **DARK_STYLE["button"],
            )
            btn.pack(side="left", expand=True)
            if i < len(buttons) - 1:
                btn.pack_configure(padx=(0, 10))  # space between buttons

            self.buttons.append(btn)

        return row_frame

    def configure_widgets(self):
        pass