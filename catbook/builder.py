from . import Markup
from . import Fonts
from . import Files
from . import Misc
from . import Book
from docx import Document
from os import remove
from os.path import exists
from pathlib import Path
from typing import Optional


class BadConfigException(Exception):
    pass


class Builder:
    def __init__(self) -> None:
        self._markup: Optional[Markup] = None
        self._fonts: Optional[Fonts] = None
        self._files: Optional[Files] = None
        self._misc: Optional[Misc] = None
        self._document: Optional[Document] = None

    # ========== PUBLIC STUFF GOES HERE

    def init(self) -> None:
        if self._markup is None:
            self._markup = Markup()
        if self._fonts is None:
            self._fonts = Fonts()
        if self._files is None:
            self._files = Files()
        if self._misc is None:
            self._misc = Misc()
        self._new_document()
        self._book: Optional[Book] = None

    @property
    def book(self) -> Optional[Book]:
        if self._book is None:
            self.init()
            self.book = Book(
                files=self._files,  # type: ignore [arg-type]
                markup=self._markup,
                fonts=self._fonts,
                document=self.doc,
            )
        return self._book

    @book.setter
    def book(self, b: Book) -> None:
        self._book = b

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

    @property
    def misc(self) -> Optional[Misc]:
        return self._misc

    @misc.setter
    def misc(self, m: Misc) -> None:
        self._misc = m

    def build(self):
        if None in [self._markup, self._fonts, self._files, self.doc]:
            self.init()
        if not self._validate():
            raise BadConfigException(
                f"Cannot start build with files config: {self.files}"
            )
        self._clean_output()
        self.book.create()
        self._save()
        self._reset()

    # ========== INTERNAL STUFF STARTS HERE

    def _validate(self) -> bool:
        print("Validating configuration")
        if self._files is None:
            print("No files config available")
            return False

        if self._files.INPUT is None:  # type: ignore[union-attr]
            print(f"No input file configured in {self._files.INPUT}")
            return False

        if not exists(self._files.INPUT):  # type: ignore[union-attr]
            print(f"No input file configured in {self._files}")  # type: ignore[union-attr]
            return False

        if self._files.FILES is None:  # type: ignore[union-attr]
            print(f"No files directory configured in {self._files}")
            return False

        if not exists(self._files.FILES):  # type: ignore[union-attr]
            print(f"Files directory does not exist at {self._files.FILES}")  # type: ignore[union-attr]
            return False

        return True

    def _new_document(self) -> None:
        document = Document()
        self.doc = document

    def _clean_output(self) -> None:
        """Cleans the output file location"""
        try:
            print(f"Cleaning {self._files.OUTPUT}")  # type: ignore[union-attr]
            remove(self._files.OUTPUT)  # type: ignore[union-attr]
        except FileNotFoundError:
            print(f"Nothing to clean configured in {self._files}")  # type: ignore[union-attr]

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
