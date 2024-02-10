import csv
from . import Files
from . import Markup
from . import Fonts
from . import Section
from . import BookMetadata
from docx import Document
import traceback
from typing import List
import os


class UnknownBookfileTypeException(Exception):
    pass


class BookfileNotFoundException(Exception):
    pass


class BookfileMistakeException(Exception):
    pass


class Book:
    def __init__(
        self, files: Files, markup: Markup, fonts: Fonts, document: Document
    ) -> None:
        self._files = files
        self._fonts = fonts
        self._markup = markup
        self._file_count = 0
        self._document = document
        self._metadata = BookMetadata()

    @property
    def files(self) -> int:
        return self._file_count

    @property
    def metadata(self) -> BookMetadata:
        return self._metadata

    def create(self) -> int:
        """returns the rows count, including comments but not blanks"""
        cnt = 0
        rows = self._get_rows()
        for row in rows:
            if len(row[0]) > 0 and row[0][0] == "#":
                pass
            else:
                try:
                    # build the book here
                    self._append_section(row)
                    self._file_count = self._file_count + 1
                except Exception as e:
                    print(f"Error: {cnt}: {row}: {e}")
                    print(traceback.format_exc())
            cnt = cnt + 1
        return cnt

    def _get_rows(self) -> List[str]:
        try:
            if self._files.INPUT.endswith(".csv"):
                return self._get_rows_csv()
            elif self._files.INPUT.endswith(".txt") or self._files.INPUT.endswith(
                ".bookfile"
            ):
                return self._get_rows_txt()
            else:
                raise UnknownBookfileTypeException(
                    f"Unknown bookfile type. Please check {self._files.INPUT}"
                )
        except FileNotFoundError:
            raise BookfileNotFoundException(
                f"Bookfile not found. Please check {self._files.INPUT}"
            )

    def _get_rows_csv(self) -> List[str]:
        rows = []
        with open(self._files.INPUT) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if len(row) == 0:
                    pass
                elif len(row[0]) > 0 and row[0][0] == "#":
                    rows.append(row[0])
                else:
                    rows.append(f"{row[0]}/{row[1]}")
        return rows

    def _get_rows_txt(self) -> List[str]:
        rows = []
        with open(self._files.INPUT) as file:
            for line in file:
                line = line.strip()
                if len(line) == 0:
                    pass
                elif len(line[0]) > 0 and line[0][0] == "#":
                    rows.append(line)
                else:
                    rows.append(line)
        return rows

    def _append_section(self, path: str):
        section_metadata = self.metadata.new_section()
        section_metadata.add_relative_file(path)
        path = f"{self._files.FILES}/{path}"
        section_metadata.FILE = path

        if not os.path.exists(path):
            raise BookfileMistakeException(f"{path} does not exist")

        file_stats = os.stat(path)
        section_metadata.CHAR_COUNT = file_stats.st_size

        with open(path, "r") as contents:
            lines = contents.readlines()
            section = Section(
                lines,
                markup=self._markup,
                fonts=self._fonts,
                document=self._document,
                metadata=section_metadata,
            )
            section.compile()
