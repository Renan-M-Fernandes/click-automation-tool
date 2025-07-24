from base_screen import BaseScreen
import tkinter as tk
import os

def exit_program():
    exit()

class MainScreen(BaseScreen):
    def __init__(self, parent, controller, config=None, loc_manager=None):

        super().__init__(parent, controller, config=config, loc_manager=loc_manager)
        self.controller = controller
        self.running_gui = False

        print(self.locale.get("LABEL_MAIN"))
        self.title_label = self.create_title_label(self.locale.get("LABEL_MAIN"))

        self.auto_button = self.create_button((self.locale.get("BUTTON_AUTOCLK")),
                                       command=lambda: self.controller.show_frame("AutoClickerScreen"))

        self.screen_button = self.create_button(self.locale.get("BUTTON_SCREENCLK"), command=self.screen_clicker)

        self.exit_button = self.create_button(self.locale.get("EXIT"), command=exit_program)

        self.language_frame = tk.Frame(self, bg=self["bg"])
        self.language_frame.pack(side="bottom", anchor="se", padx=10, pady=10)

        self.flags = {
            "en": tk.PhotoImage(file="assets/flags/en.png"),
            "pt": tk.PhotoImage(file="assets/flags/pt.png"),
        }

        #self.current_lang = self.config.get("language", "en")
        self.current_lang = "en"
        self.flag_button = tk.Button(
            self.language_frame, image=self.flags[self.current_lang],
            command=self.toggle_language_menu,borderwidth=0, highlightthickness=0, relief="flat", bd=0, bg=self["bg"], activebackground=self["bg"]
        )

        self.flag_button.pack()

        self.lang_menu = None

    def refresh(self):
        self.title_label.config(text=self.locale.get("LABEL_MAIN"))
        self.auto_button.config(text=self.locale.get("BUTTON_AUTOCLK"))
        self.screen_button.config(text=self.locale.get("BUTTON_SCREENCLK"))
        self.exit_button.config(text=self.locale.get("EXIT"))

    def toggle_language_menu(self):
        if self.lang_menu:
            self.lang_menu.destroy()
            self.lang_menu = None
            return

        self.lang_menu = tk.Frame(self.language_frame, bg=self["bg"])
        self.lang_menu.pack()

        for code, icon in self.flags.items():
            if code != self.current_lang:
                btn = tk.Button(self.lang_menu, image=icon, bd=0, bg=self["bg"], activebackground=self["bg"],
                                command=lambda c=code: self.set_language(c))
                btn.pack()

    def set_language(self, code):
        self.current_lang = code
        self.config_data["language"] = code
        self.locale.set_language(code)  # Assuming your locale handler has a method like this
#        self.controller.save_config()   # Update your config saving logic if needed
        self.controller.refresh_all_screens()  # You can implement a method to rebuild the UI with the new language
        self.flag_button.config(image=self.flags[code])
        if self.lang_menu:
            self.lang_menu.destroy()
            self.lang_menu = None


    def screen_clicker(self):
            self.show_message_box(self.locale.get("MSG_IN_PROGRESS_LABEL"), self.locale.get("MSG_IN_PROGRESS"))