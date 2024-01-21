import csv
from . import Files
from . import Markup
from . import Fonts
from . import Section
from docx import Document
import traceback


class Book:
    def __init__(
        self, files: Files, markup: Markup, fonts: Fonts, document: Document
    ) -> None:
        self._files = files
        self._fonts = fonts
        self._markup = markup
        self._file_count = 0
        self._document = document

    @property
    def files(self) -> int:
        return self._file_count

    def create(self) -> int:
        """returns the rows count, including comments and blanks"""
        with open(self._files.INPUT) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            rows = 0
            for row in csv_reader:
                if len(row) == 0:
                    pass
                elif len(row[0]) > 0 and row[0][0] == "#":
                    pass
                else:
                    path = None
                    try:
                        path = f"{row[0]}/{row[1]}"

                        # build the book here
                        self._append_section(path)

                        self._file_count = self._file_count + 1
                    except Exception as e:
                        print(f"Error: {row}: {rows}: {path}: {e}")
                        print(traceback.format_exc())
                rows = rows + 1
        return rows

    def _append_section(self, path: str):
        path = f"{self._files.FILES}/{path}"
        with open(path, "r") as contents:
            lines = contents.readlines()
            section = Section(
                lines, markup=self._markup, fonts=self._fonts, document=self._document
            )
            section.compile()
