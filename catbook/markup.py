from dataclasses import dataclass


@dataclass
class Markup:
    JUMP: str = "***"
    CHAPTER_TITLE: str = "~"
    BOOK_TITLE: str = "~~"
    NEW_SECTION: str = ">"
    BLOCK: str = "|"
    QUOTED_LINE: str = '"'
    WORD_HIGHLIGHT: str = "|"
