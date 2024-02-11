from dataclasses import dataclass, field
from typing import List, Optional
from . import Markup
from . import Metadata


class SectionContentException(Exception):
    pass


@dataclass
class SectionMetadata(Metadata):
    FILE: Optional[str] = None
    RELATIVE_PATH: Optional[str] = None
    NAME: Optional[str] = None
    FIRST_LINE: Optional[str] = None
    FILE_LINE_COUNT: int = 0
    STAND_ALONE: bool = False
    CHAR_COUNT: int = 0
    WORD_COUNT: int = 0
    WORDS: List[str] = field(default_factory=list)

    def unique_words_count(self) -> int:
        words = {}
        for w in self.WORDS:
            words[w] = w
        return len(words)

    def set_first_line(self, markup: Markup, line: str) -> None:
        if line is None:
            raise SectionContentException("Line cannot be None")
        line = line.strip()
        if (
            line.find(markup.NEW_SECTION) == 0
            or line.find(markup.CHAPTER_TITLE) == 0
            or line.find(markup.BOOK_TITLE) == 0
        ):
            self.STAND_ALONE = True
        self.FIRST_LINE = line

    def add_relative_file(self, name: str) -> None:
        if name is None:
            raise SectionContentException("Name cannot be None")
        self.RELATIVE_PATH = name
        slash = name.rfind("/")
        if slash > -1:
            name = name[slash + 1 :]
        dot = name.rfind(".")
        if dot > -1:
            name = name[0:dot]
        self.NAME = name
