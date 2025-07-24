import tkinter as tk
import gui_main
import gui_config
import gui_auto_clicker
import base_screen
from config_handler import load_config
from locale_handler import LocalizationManager
from gui_config import ConfigScreen
from gui_auto_clicker import AutoClickerScreen

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        config = load_config()
        self.locale_manager = LocalizationManager()
        self.frames = {}
        loc_manager = LocalizationManager(lang_code="en")
        self.title(loc_manager.get("TITLE_MAIN"))

        for F in (gui_main.MainScreen, gui_config.ConfigScreen, gui_auto_clicker.AutoClickerScreen, base_screen.BaseScreen):
            name = F.__name__
            frame = F(self.container, self, config=config, loc_manager=loc_manager)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainScreen")

    def show_frame(self, name):
        # Oculta a tela atual, se houver
        if hasattr(self, "current_frame") and hasattr(self.current_frame, "on_hide"):
            self.current_frame.on_hide()

        # Mostra a nova tela
        frame = self.frames[name]
        frame.tkraise()

        # Atualiza referência da tela atual
        self.current_frame = frame

        # Chama o método de exibição, se existir
        if hasattr(frame, "on_show"):
            frame.on_show()

    def refresh_all_screens(self):
        for frame in self.frames.values():
            if hasattr(frame, "refresh"):
                frame.refresh()



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()