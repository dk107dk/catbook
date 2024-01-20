from configparser import ConfigParser
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

    def __post_init__(self):
        self._config = ConfigParser()
        self._load_config()

    def _load_config(self):
        markup = "markup.ini"
        if path.isfile(markup):
            self._config.read(markup)
            section = "markup"
            self.JUMP = self._config[section]["jump"]
            self.CHAPTER_TITLE = self._config[section]["chapter_title"]
            self.BOOK_TITLE = self._config[section]["book_title"]
            self.NEW_SECTION = self._config[section]["new_section"]
            self.BLOCK = self._config[section]["block"]
            self.QUOTED_LINE = self._config[section]["quoted_line"]
            self.WORD_HIGHLIGHT = self._config[section]["word_highlight"]
        else:
            print(f"No {markup} file found. Using default markup markers")
