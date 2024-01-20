from configparser import RawConfigParser
from dataclasses import dataclass
from os import path


@dataclass
class Files:
    INPUT: str = "contents.csv"
    OUTPUT: str = "./out/out.docx"
    FILES: str = "../texts"
    CONFIG: str = "config/files.ini"

    def __post_init__(self):
        self._config = RawConfigParser()
        self._load_config()

    def reload(self):
        self._load_config()

    def _load_config(self):
        if path.isfile(self.CONFIG):
            self._config.read(self.CONFIG)
            section = "files"
            try:
                self.INPUT = self._config[section]["input"]
            except KeyError:
                pass
            try:
                self.OUTPUT = self._config[section]["output"]
            except KeyError:
                pass
            try:
                self.FILES = self._config[section]["files"]
            except KeyError:
                pass
        else:
            print(f"No files {self.CONFIG} file found. Using default file locations.")
