from dataclasses import dataclass, field
from typing import List, Optional, Dict, cast
from . import SectionMetadata
from . import Files
from . import Metadata


@dataclass
class BookMetadata(Metadata):
    FILES: Files
    SECTIONS: List[SectionMetadata] = field(default_factory=list)
    TITLE: str = ""
    AUTHOR: str = ""

    def __post_init__(self):
        self.seek_metadata()

    def sections_count(self) -> int:
        return len(self.SECTIONS)

    def seek_metadata(self) -> None:
        if self.FILES is None or self.FILES.INPUT is None:
            return
        if self.TITLE == "" or self.TITLE is None:
            title = self._seek("TITLE")
            if title is not None:
                self.TITLE = title
        if self.AUTHOR == "" or self.AUTHOR is None:
            author = self._seek("AUTHOR")
            if author is not None:
                self.AUTHOR = author

    def _seek(self, token: str) -> Optional[str]:
        if token not in ["TITLE", "AUTHOR"]:
            raise Exception("token must be either title or author")
        with open(self.FILES.INPUT) as file:
            for line in file:
                if line[0] == "#" and line.find(token) > 0:
                    return line[(line.find(token) + len(token) + 1) :].strip()
        return None

    @property
    def count(self) -> int:
        return len(self.SECTIONS)

    @property
    def stand_alone_count(self) -> int:
        count = 0
        for s in self.SECTIONS:
            if s.STAND_ALONE:
                count = count + 1
        return count

    def new_section(self):
        section = SectionMetadata(self)
        section.BOOK_METADATA = self
        self.SECTIONS.append(section)
        return section

    def last_section(self, section: Metadata) -> Optional[Metadata]:
        index = self.SECTIONS.index(cast(SectionMetadata, section))
        if index == 0:
            return None
        else:
            return self.SECTIONS[index - 1]

    def next_section(self, section: Metadata) -> Optional[Metadata]:
        index = self.SECTIONS.index(cast(SectionMetadata, section))
        if index >= len(self.SECTIONS) - 1:
            return None
        else:
            return self.SECTIONS[index - 1]

    @property
    def word_count(self) -> int:
        words = 0
        for s in self.SECTIONS:
            words += s.WORD_COUNT
        return words

    def unique_words_count(self) -> int:
        return len(self.words())

    def words(self) -> Dict[str, int]:
        words: Dict[str, int] = {}
        for s in self.SECTIONS:
            for word in s.WORDS:
                if word in words:
                    words[word] = words[word] + 1
                else:
                    words[word] = 1
        return words

    def paragraphs_count(self) -> int:
        count = 0
        for s in self.SECTIONS:
            count += s.PARAGRAPH_COUNT
        return count
