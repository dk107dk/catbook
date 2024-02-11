from dataclasses import dataclass, field
from typing import List, Optional, Dict
from . import SectionMetadata
from . import Files
from . import Metadata


@dataclass
class BookMetadata(Metadata):
    FILES: Files
    SECTIONS: List[SectionMetadata] = field(default_factory=list)
    TITLE: str = ""
    AUTHOR: str = ""

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
        section = SectionMetadata()
        self.SECTIONS.append(section)
        return section

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
