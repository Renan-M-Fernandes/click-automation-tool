from base_screen import BaseScreen

def exit_program():
    exit()

class MainScreen(BaseScreen):
    def __init__(self, parent, controller, config=None):

        super().__init__(parent, controller, config=config)
        self.controller = controller
        self.running_gui = False

        self.create_title_label("Choose Your Tool")

        self.auto_button = self.create_button(("Auto Clicker"),
                                       command=lambda: self.controller.show_frame("AutoClickerScreen"))

        self.screen_button = self.create_button("Screen Clicker", command=self.screen_clicker)

        self.exit_button = self.create_button("EXIT", command=exit_program)

    def screen_clicker(self):
        self.show_message_box("Warning", "This tool has not yet been implemented!")