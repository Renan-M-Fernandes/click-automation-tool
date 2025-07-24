import tkinter as tk

from base_screen import BaseScreen
from config_handler import save_config


class ConfigScreen(BaseScreen):
    def __init__(self, parent, controller, config=None):
        super().__init__(parent, controller, config=config)
        self.create_title_label("Config Screen")

        # Hotkey
        self.create_label("Choose hotkey:")
        self.hotkey_entry = self.create_entry_alpha()
        self.hotkey_entry.bind("<FocusIn>", self.start_listening_hotkey)
        self.hotkey_entry.bind("<FocusOut>", self.stop_listening_hotkey)
        self.hotkey_entry.insert(0, self.config_data.get("hotkey"))

        # Left or Right click
        self.create_label("Click button:")
        self.click_button_combo = self.create_combo_box(
            values=["Left Click", "Right Click"]
        )
        self.click_button_combo.set(self.config_data.get("click_button"))

        # Single or Double click
        self.create_label("Click type:")
        self.click_type_combo = self.create_combo_box(
            values=["Single Click", "Double Click"]
        )
        self.click_type_combo.set(self.config_data.get("click_type"))

        # Interval input
        self.create_label("Interval between clicks (seconds):")
        self.interval_entry = self.create_entry_num()
        self.interval_entry.insert(0, self.config_data.get("interval"))
        # Buttons side by side
        self.create_button_row([
            {"text": "Save", "command": self.save_config, "width": 12},
            {"text": "Back", "command": self.exit_config, "width": 12},
        ])

        self.hotkey_binding = None

    def save_config(self):
        data = {
            "hotkey": self.hotkey_entry.get(),
            "click_button": self.click_button_combo.get(),
            "click_type": self.click_type_combo.get(),
            "interval": float(self.interval_entry.get())
        }
        save_config(data)
        print("Config saved!")
        self.show_message_box("Saved", "Configuration saved successfully!")

    def exit_config(self):
        self.hotkey_entry.master.focus()
        self.controller.show_frame("AutoClickerScreen")

    def on_show(self):
        pass

    def start_listening_hotkey(self, event=None):
        if self.hotkey_binding is None:
            self.hotkey_binding = self.hotkey_entry.bind("<Key>", self.handle_key)

    def stop_listening_hotkey(self, event=None):
        if self.hotkey_binding is not None:
            self.hotkey_entry.unbind("<Key>", self.hotkey_binding)
            self.hotkey_binding = None

    def handle_key(self, event):
        key = event.keysym  # or event.char for lowercase
        self.hotkey_entry.delete(0, tk.END)
        self.hotkey_entry.insert(0, key)
        print(f"Hotkey set to: {key}")
        return "break"