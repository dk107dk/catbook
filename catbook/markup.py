from configparser import RawConfigParser
from dataclasses import dataclass
from os import path
from typing import Optional


@dataclass
class Markup:
    """First line, first chars. A JUMP creates a break
    within a chapter by adding an untitled section
    separated from the preceding section by an
    ASTERISM. Often people use three widely spaced
    stars or dots as the indicator. The JUMP markup must
    be three characters."""

    JUMP: str = "***"

    """ First line, first char. a CHAPTER_TITLE is a grouping
        that is below book and above section. The chapter
        title markup must be one character. """
    CHAPTER_TITLE: str = "~"

    """ First line, first char. A BOOK_TITLE is the top
        unit. From a TOC perspective, it contains chapters and
        sections. The book title markup must be two characters. """
    BOOK_TITLE: str = "~~"

    """ First line, first char. Forces the section to start
        on a new page """
    NEW_SECTION: str = ">"

    """ Any line, first char. Text that is set off from
        the rest of the quoted and unquoted paragraphs.
        could be used for inserting the text of a document
        into a narrative. """
    BLOCK: str = "|"

    """ Any line, first char. a paragraph of quoted text.
        This markup is also useful for forcing a blank line.
        to do that, make it the first character of an
        otherwise blank line.  """
    QUOTED_LINE: str = '"'

    """ Around any word or words. highlights the words
        between two of the marks in a paragraph. for e.g., in
        italics. Assuming | is used for both highlights and
        blocks, if a highlight begins with the first word of
        a paragraph it will look like a block. in that case
        use a double highlight mark, as in: ||some words|. """
    WORD_HIGHLIGHT: str = "|"

    """ The text that will be used as the asterism when
        a JUMP is found """
    ASTERISM: str = "*                           ⁂                           *"

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
            try:
                self.ASTERISM = self._config[section]["asterism"]
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
