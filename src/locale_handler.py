import json
import os

class LocalizationManager:
    def __init__(self, lang_code="en", locales_path="locales"):
        self.locales_path = locales_path
        self.lang_code = None
        self.strings = {}
        self.set_language(lang_code)

    def load_language(self, lang_code):
        path = os.path.join(self.locales_path, f"{lang_code}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[Localization] File for '{lang_code}' not found.")
            return None

    def set_language(self, lang_code):
        strings = self.load_language(lang_code)
        if strings:
            self.strings = strings
            self.lang_code = lang_code
        else:
            # Fallback para inglês
            if lang_code != "en":
                print("[Localization] Falling back to English.")
                self.set_language("en")
            else:
                self.strings = {}
                self.lang_code = "en"

    def get(self, key):
        return self.strings.get(key, f"[{key}]")