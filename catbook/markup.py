from configparser import RawConfigParser
from dataclasses import dataclass
from os import path
from typing import Optional


@dataclass
class Markup:
    JUMP: str = "***"
    CHAPTER_TITLE: str = "~"
    BOOK_TITLE: str = "~~"
    NEW_SECTION: str = ">"
    BLOCK: str = "|"
    QUOTED_LINE: str = '"'
    WORD_HIGHLIGHT: str = "|"
    CONFIG: str = "markup.ini"

    def __post_init__(self):
        self._config = RawConfigParser()
        self._load_config()

    def reload(self):
        self._load_config()

    def _load_config(self):
        if path.isfile(self.CONFIG):
            self._config.read(self.CONFIG)
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
            print(f"No markup {self.CONFIG} file found. Using default markup markers.")

    def _is_quote(self, line: str, line_number: int, lines: int) -> bool:
        ll = len(line)
        if ll == 0:
            return False
        if line[0] != self.QUOTED_LINE:
            return False
        if line_number >= lines:  # why would this happen?
            return False
        return True

    def _is_block(self, line: str, line_number: int, lines: int) -> Optional[bool]:
        ll = len(line)
        if ll == 0:
            return False
        if line[0] == self.BLOCK and ll > 1 and line[1] == self.BLOCK:
            return None
        if line[0] != self.BLOCK:
            return False
        if line_number >= lines:  # why would this happen?
            return False
        return True
