from . import Markup
from . import Fonts
from . import Files
from docx import Document
from os import remove
from os.path import exists
from pathlib import Path
from typing import Optional


class NoInputException(Exception):
    pass


class Builder:
    def __init__(self):
        self._markup: Optional[Markup] = None
        self._fonts: Optional[Fonts] = None
        self._files: Optional[Files] = None
        self._document: Optional[Document] = None

    # ========== PUBLIC STUFF GOES HERE

    def init(self) -> None:
        self._markup = Markup()
        self._fonts = Fonts()
        self._files = Files()
        self._new_document()
        print("Done initalizing")

    @property
    def doc(self) -> Optional[Document]:
        return self._document

    @doc.setter
    def doc(self, d: Document) -> None:
        self._document = d

    @property
    def files(self) -> Optional[Files]:
        return self._files

    @files.setter
    def files(self, f: Files) -> None:
        self._files = f

    def build(self):
        print("Starting build")
        if None in [self._markup, self._fonts, self._files, self.doc]:
            print("Initialization required")
            self.init()
        if not self._validate():
            raise NoInputException(
                f"Cannot start build without an input file: {self.files}"
            )
        self._clean_output()

        # build happens here

        self._save()
        self._reset()

    # ========== INTERNAL STUFF STARTS HERE

    def _validate(self) -> bool:
        valid = self._files is not None
        if not valid:
            print("No files config available")
        valid = self._files.INPUT is not None  # type: ignore[union-attr]
        if not valid:
            print(f"No input file configured in {self._files}")
        valid = exists(self._files.INPUT)  # type: ignore[union-attr]
        if not valid:
            print(f"No input file at {self._files.INPUT}")  # type: ignore[union-attr]
        return valid

    def _new_document(self) -> None:
        document = Document()
        self.doc = document

    def _clean_output(self) -> None:
        """Cleans the output file location"""
        print(f"Cleaning {self._files.OUTPUT}")  # type: ignore[union-attr]
        try:
            remove(self._files.OUTPUT)  # type: ignore[union-attr]
        except FileNotFoundError:
            print(f"Nothing to clean at {self._files.OUTPUT}")  # type: ignore[union-attr]

    def _reset(self) -> None:
        """removes the config and doc in case this instance gets used again"""
        self._markup = None
        self._fonts = None
        self._files = None
        self._document = None

    def _save(self):
        """not Windows safe!"""
        print(f"Saving document to {self._files.OUTPUT}")
        if "/" in self._files.OUTPUT:
            dirs = self._files.OUTPUT[0 : self._files.OUTPUT.rindex("/")]
            Path(dirs).mkdir(parents=True, exist_ok=True)
        self.doc.save(self._files.OUTPUT)
