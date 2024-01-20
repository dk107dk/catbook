from configparser import RawConfigParser
from dataclasses import dataclass
from os import path


@dataclass
class Fonts:
    QUOTE: str = "Times New Roman"
    BLOCK: str = "Courier New"
    TITLE: str = "Times New Roman"
    BODY: str = "Times New Roman"
    CONFIG: str = "config/fonts.ini"

    def __post_init__(self):
        self._config = RawConfigParser()
        self._load_config()

    def reload(self):
        self._load_config()

    def _load_config(self):
        if path.isfile(self.CONFIG):
            self._config.read(self.CONFIG)
            section = "fonts"
            try:
                self.QUOTE = self._config[section]["quote"]
            except KeyError:
                pass
            try:
                self.BLOCK = self._config[section]["block"]
            except KeyError:
                pass
            try:
                self.TITLE = self._config[section]["title"]
            except KeyError:
                pass
            try:
                self.BODY = self._config[section]["body"]
            except KeyError:
                pass
        else:
            print(f"No fonts {self.CONFIG} file found. Using default fonts.")
