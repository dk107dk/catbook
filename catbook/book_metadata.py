from dataclasses import dataclass, field
from typing import List, Optional
from . import SectionMetadata


@dataclass
class BookMetadata:
    SECTIONS: List[SectionMetadata] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.SECTIONS)

    def new_section(self):
        section = SectionMetadata()
        self.SECTIONS.append(section)
        return section

    def word_count(self):
        words = 0
        for s in self.SECTIONS:
            words += s.WORD_COUNT
        return words

    def words(self):
        words = {}
        for s in self.SECTIONS:
            for word in s.WORDS:
                if word in words:
                    words[word] = words[word] + 1
                else:
                    words[word] = 1
        return words
