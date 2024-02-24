from dataclasses import dataclass, field
from typing import List, Optional
from . import Markup
from . import Metadata


class SectionContentException(Exception):
    pass


@dataclass
class SectionMetadata(Metadata):
    BOOK_METADATA: Metadata
    FILE: Optional[str] = None
    RELATIVE_PATH: Optional[str] = None
    NAME: Optional[str] = None
    FIRST_LINE: Optional[str] = None
    FILE_LINE_COUNT: int = 0
    STAND_ALONE: bool = False
    CHAR_COUNT: int = 0
    WORD_COUNT: int = 0
    PARAGRAPH_COUNT: int = 0
    WORDS: List[str] = field(default_factory=list)
    NEW_SECTION: bool = False
    BOOK: bool = False
    CHAPTER: bool = False
    JUMP: bool = False

    def __str__(self):
        me = "SectionMetadata:\n"
        me += f"\tSECTION: {len(self.BOOK_METADATA.SECTIONS)},\n"
        me += f"\tFILE: {self.FILE},\n"
        me += f"\tRELATIVE_PATH: {self.RELATIVE_PATH},\n"
        me += f"\tNAME: {self.NAME},\n"
        me += f"\tFIRST_LINE: {self.FIRST_LINE},\n"
        me += f"\tSTAND_ALONE: {self.STAND_ALONE},\n"
        me += f"\tFILE_LINE_COUNT: {self.FILE_LINE_COUNT},\n"
        me += f"\tCHAR_COUNT: {self.CHAR_COUNT},\n"
        me += f"\tWORD_COUNT: {self.WORD_COUNT},\n"
        me += f"\tPARAGRAPH_COUNT: {self.PARAGRAPH_COUNT},\n"
        me += f"\tBOOK: {self.BOOK},\n"
        me += f"\tCHAPTER: {self.CHAPTER},\n"
        me += f"\tNEW_SECTION: {self.NEW_SECTION},\n"
        me += f"\tJUMP: {self.JUMP}"
        return me

    def last_section(self) -> Metadata:
        return self.BOOK_METADATA.last_section(self)  # type: ignore

    def is_book_or_chapter(self) -> bool:
        return self.CHAPTER or self.BOOK

    def unique_words_count(self) -> int:
        words = {}
        for w in self.WORDS:
            words[w] = w
        return len(words)

    def set_first_line(self, markup: Markup, line: str) -> None:
        if markup is None:
            raise SectionContentException("Markup cannot be None")
        if line is None:
            raise SectionContentException("Line cannot be None")
        line = line.strip()
        """
        if (
            line.find(markup.NEW_SECTION) == 0
            or line.find(markup.CHAPTER_TITLE) == 0
            or line.find(markup.BOOK_TITLE) == 0
        ):
            self.STAND_ALONE = True
        """
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
