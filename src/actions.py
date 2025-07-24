import threading

import pyautogui

class Autoclicker ():
    def __init__(self, config):
        self.config = config
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._click_loop)
            self.thread.start()



    def stop(self):
        self.running = False

    def _click_loop(self):
        interval = self.config.get("interval")
        while self.running:
            print("Clicou")
            pyautogui.click()
            pyautogui.PAUSE = interval