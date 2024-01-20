from . import Markup
from . import Fonts
from . import Files
from docx import Document
from os import remove


class Builder:
    def __init__(self):
        self._markup: Markup = None
        self._fonts: Fonts = None
        self._files: Files = None
        self._document: Document = None

    def init(self):
        self._markup = Markup()
        self._fonts = Fonts()
        self._files = Files()
        self._clean()
        self._new_document()

    @property
    def doc(self) -> Document:
        return self._document

    @doc.setter
    def doc(self, d: Document) -> None:
        self._document = d

    def build(self):
        if None in [self._markup, self._fonts, self._files, self.doc]:
            print("Initializing")
            self.init()

    # ========== INTERNAL STUFF STARTS HERE

    def _new_document(self):
        document = Document()
        self.doc = document

    def _clean(self):
        print(f"Cleaning {self._files.OUTPUT}")
        try:
            remove(self._files.OUTPUT)
        except FileNotFoundError:
            print(f"Nothing to clean at {self._files.OUTPUT}")
