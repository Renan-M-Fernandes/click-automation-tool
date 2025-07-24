import tkinter as tk

from base_screen import BaseScreen
from config_handler import save_config


class ConfigScreen(BaseScreen):
    def __init__(self, parent, controller, config=None, loc_manager=None):
        super().__init__(parent, controller, config=config, loc_manager=loc_manager)
        self.title_label = self.create_title_label(self.locale.get("CONFIGURATION_BUTTON"))

        self.click_button_options = {
            "left": self.locale.get("VALUE_CLK_BUTTON_1"),
            "right": self.locale.get("VALUE_CLK_BUTTON_2")
        }
        self.rev_click_button_options = {v: k for k, v in self.click_button_options.items()}

        self.click_type_options = {
            "single": self.locale.get("VALUE_CLK_TYPE_1"),
            "double": self.locale.get("VALUE_CLK_TYPE_2")
        }
        self.rev_click_type_options = {v: k for k, v in self.click_type_options.items()}

        # Hotkey
        self.hotkey_label = self.create_label(self.locale.get("LABEL_HOTKEY"))
        self.hotkey_entry = self.create_entry_alpha()
        self.hotkey_entry.bind("<FocusIn>", self.start_listening_hotkey)
        self.hotkey_entry.bind("<FocusOut>", self.stop_listening_hotkey)
        self.hotkey_entry.insert(0, self.config_data.get("hotkey"))

        # Left or Right click
        self.clk_button = self.create_label(self.locale.get("LABEL_CLK_BUTTON"))
        self.click_button_combo = self.create_combo_box(
            values=list(self.click_button_options.values())
        )
        self.click_button_combo.set(
            self.click_button_options.get(self.config_data.get("click_button", "left"))
        )

        # Single or Double click
        self.type_button = self.create_label(self.locale.get("LABEL_CLK_TYPE"))
        self.click_type_combo = self.create_combo_box(
            values=list(self.click_type_options.values())
        )
        self.click_type_combo.set(
            self.click_type_options.get(self.config_data.get("click_type", "single"))
        )

        # Interval input
        self.interval_label = self.create_label(self.locale.get("LABEL_CLK_INTERVAL"))
        self.interval_entry = self.create_entry_num()
        self.interval_entry.insert(0, self.config_data.get("interval"))
        # Buttons side by side
        self.button_row = self.create_button_row([
            {"text": self.locale.get("SAVE"), "command": self.save_config, "width": 12},
            {"text": self.locale.get("BACK"), "command": self.exit_config, "width": 12},
        ])

        self.hotkey_binding = None

    def refresh(self):
        self.title_label.config(text=self.locale.get("CONFIGURATION_BUTTON"))
        self.hotkey_label.config(text=self.locale.get("LABEL_HOTKEY"))
        self.clk_button.config(text=self.locale.get("LABEL_CLK_BUTTON"))
        self.type_button.config(text=self.locale.get("LABEL_CLK_TYPE"))
        self.interval_label.config(text=self.locale.get("LABEL_CLK_INTERVAL"))
        self.buttons[0].config(text=self.locale.get("SAVE"))
        self.buttons[1].config(text=self.locale.get("BACK"))

        # Rebuild translation maps
        self.click_button_options = {
            "left": self.locale.get("VALUE_CLK_BUTTON_1"),
            "right": self.locale.get("VALUE_CLK_BUTTON_2")
        }
        self.rev_click_button_options = {v: k for k, v in self.click_button_options.items()}

        self.click_type_options = {
            "single": self.locale.get("VALUE_CLK_TYPE_1"),
            "double": self.locale.get("VALUE_CLK_TYPE_2")
        }
        self.rev_click_type_options = {v: k for k, v in self.click_type_options.items()}

        # Refresh combo boxes
        self.click_button_combo.config(values=list(self.click_button_options.values()))
        self.click_button_combo.set(
            self.click_button_options.get(self.config_data.get("click_button", "left"))
        )

        self.click_type_combo.config(values=list(self.click_type_options.values()))
        self.click_type_combo.set(
            self.click_type_options.get(self.config_data.get("click_type", "single"))
        )

    def save_config(self):
        data = {
            "hotkey": self.hotkey_entry.get(),
            "click_button": self.rev_click_button_options.get(self.click_button_combo.get(), "left"),
            "click_type": self.rev_click_type_options.get(self.click_type_combo.get(), "single"),
            "interval": float(self.interval_entry.get())
        }
        save_config(data)
        print("Config saved!")
        self.show_message_box(self.locale.get("MSG_SAVE_LABEL"), self.locale.get("MSG_SAVE"))

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