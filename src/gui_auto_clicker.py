import threading
import time
import keyboard
from actions import Autoclicker
from styles import DARK_STYLE
from base_screen import BaseScreen

class AutoClickerScreen(BaseScreen):
    def __init__(self, parent, controller, config=None, loc_manager=None):
        super().__init__(parent, controller, config=config, loc_manager=loc_manager)
        self.configure(bg=DARK_STYLE["colors"]["bg_main"])
        self.title_label = self.create_title_label(self.locale.get("TITLE_AUTOCLK"))

        self.controller = controller
        self.clicker = Autoclicker(config)
        self.running_gui = False
        self.running = False

        self.start_button = self.create_button(self.locale.get("START_BUTTON") + " - " + self.config_data.get("hotkey"), command=self.toggle_clicking)

        self.config_button = self.create_button(self.locale.get("CONFIGURATION_BUTTON"), command=self.config_screen)

        self.prev_button = self.create_button(self.locale.get("BACK"), command=self.previous_screen)

    def refresh(self):
        self.title_label.config(text=self.locale.get("TITLE_AUTOCLK"))
        self.start_button.config(text=self.locale.get("START_BUTTON"))
        self.config_button.config(text=self.locale.get("CONFIGURATION_BUTTON"))
        self.prev_button.config(text=self.locale.get("BACK"))

    def on_show(self):
        if not hasattr(self, "thread") or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self._keyboard_loop, daemon=True)
            self.thread.start()

    def toggle_clicking(self):
        if hasattr(self, "_toggle_locked") and self._toggle_locked:
            return

        self._toggle_locked = True
        self.after(1000, lambda: setattr(self, "_toggle_locked", False))  # libera após 100ms

        if not self.running_gui:
            self.start_clicking()
        else:
            self.stop_clicking()

    def start_clicking(self):
        print("AutoClicker Started")
        self.running_gui = True
        self.clicker.start()
        self.start_button.config(text=self.locale.get("STOP_BUTTON") + " - " + self.config_data.get("hotkey"))

    def stop_clicking(self):
        print("AutoClicker Stopped")
        self.running_gui = False
        self.clicker.stop()
        self.start_button.config(text=self.locale.get("START_BUTTON") + " - " + self.config_data.get("hotkey"))

    def previous_screen(self):
        if self.running:
            self.stop_clicking()
        self.controller.show_frame("MainScreen")

    def config_screen(self):
        self.running = False
        self.controller.show_frame("ConfigScreen")

    def _keyboard_loop(self):
        key_was_pressed = False
        while self.running:
            if keyboard.is_pressed(self.config_data.get("hotkey")):
                if not key_was_pressed:
                    key_was_pressed = True
                    if not self.running_gui:
                        print("entrou")
                        self.start_clicking()
                    else:
                        print("entrou")
                        self.stop_clicking()
            else:
                key_was_pressed = False
            time.sleep(0.01)