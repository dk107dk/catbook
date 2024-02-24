import abc
from . import Markup
from . import Fonts
from . import SectionMetadata
from . import BookMetadata
from . import Metadata
from docx import Document
from typing import List, Optional, Union, Any


class Section(metaclass=abc.ABCMeta):
    def __init__(
        self,
        lines: List[str],
        markup: Markup,
        fonts: Fonts,
        document: Document,
        metadata: Metadata,
    ) -> None:
        self._lines: List[str] = lines
        self._fonts: Fonts = fonts
        self._markup: Markup = markup
        self._document: Document = document
        self._block: Optional[List[Optional[str]]] = None
        self._quote: Optional[List[Optional[str]]] = None
        self._part_break: bool = False
        self._last_was_break = False
        self._metadata = metadata

    @property
    def doc(self) -> Document:
        return self._document

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @property
    def markup(self) -> Markup:
        return self._markup

    @abc.abstractmethod
    def compile(self) -> bool:
        pass
