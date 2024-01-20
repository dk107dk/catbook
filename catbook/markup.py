from configparser import RawConfigParser
from dataclasses import dataclass
from os import path


@dataclass
class Markup:
    JUMP: str = "***"
    CHAPTER_TITLE: str = "~"
    BOOK_TITLE: str = "~~"
    NEW_SECTION: str = ">"
    BLOCK: str = "|"
    QUOTED_LINE: str = '"'
    WORD_HIGHLIGHT: str = "|"
    MARKUP_CONFIG: str = "markup.ini"

    def __post_init__(self):
        self._config = RawConfigParser()
        self._load_config()

    def reload(self):
        self._load_config()

    def _load_config(self):
        if path.isfile(self.MARKUP_CONFIG):
            self._config.read(self.MARKUP_CONFIG)
            section = "markup"
            try:
                self.JUMP = self._config[section]["jump"]
            except KeyError:
                pass
            try:
                self.CHAPTER_TITLE = self._config[section]["chapter_title"]
            except KeyError:
                pass
            try:
                self.BOOK_TITLE = self._config[section]["book_title"]
            except KeyError:
                pass
            try:
                self.NEW_SECTION = self._config[section]["new_section"]
            except KeyError:
                pass
            try:
                self.BLOCK = self._config[section]["block"]
            except KeyError:
                pass
            try:
                self.QUOTED_LINE = self._config[section]["quoted_line"]
            except KeyError:
                pass
            try:
                self.WORD_HIGHLIGHT = self._config[section]["word_highlight"]
            except KeyError:
                pass
        else:
            print(f"No {self.MARKUP_CONFIG} file found. Using default markup markers")
