import csv
from . import Files
from . import Markup
from . import Fonts
from . import Section
from . import RegularSection
from . import MetadataSection
from . import BookMetadata
from docx import Document
import traceback
from typing import List, Optional
import os
from docxcompose.composer import Composer
from cdocs.cdocs import Cdocs
import logging


class UnknownBookfileTypeException(Exception):
    pass


class BookfileNotFoundException(Exception):
    pass


class BookfileMistakeException(Exception):
    pass


class Book:
    def __init__(
        self,
        files: Files,
        markup: Optional[Markup],
        fonts: Optional[Fonts],
        document: Document,
    ) -> None:
        self._files = files
        self._fonts = fonts
        self._markup = markup
        self._file_count = 0
        self._document = document
        self._metadata = BookMetadata(FILES=files)

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
        logging.info(f"book.create: rows: {rows}")
        for row in rows:
            logging.info(f"book.create: row: {row}")
            row = row.strip()
            if len(row) > 0 and row[0] == "#":
                self._check_for_inserts(row)
                self._check_for_metadata(row)
                self._check_for_page_break(row)
                cnt = cnt + 1
            elif len(row) > 0:
                logging.info(f"book.create appending {row}")
                self._append_section(row)
                self._file_count = self._file_count + 1
                cnt = cnt + 1
            else:
                logging.info("book.create: row {cnt} is ''")
        return cnt

    def _get_rows(self) -> List[str]:
        try:
            cd = self._files.INPUT[0:6] if len(self._files.INPUT) > 5 else ""
            if not self._files.INPUT.endswith(".bookfile") and cd != "cdocs:":
                raise UnknownBookfileTypeException(
                    f"Unknown bookfile type. Please check {self._files.INPUT}"
                )
            if cd == "cdocs:":
                return self._get_rows_cdocs()
            else:
                return self._get_rows_txt()
        except FileNotFoundError:
            raise BookfileNotFoundException(
                f"Bookfile not found. Please check {self._files.INPUT}"
            )

    @property
    def cdocs(self) -> Cdocs:
        root = self._files.FILES[6:]
        cdocs = Cdocs(root)
        return cdocs

    def _get_rows_cdocs(self) -> List[str]:
        logging.info("book._get_rows_cdocs: getting cdocs rows")
        docpath = (
            self._files.INPUT[6:]
            if self._files.INPUT[0:6] == "cdocs:"
            else self._files.INPUT
        )
        logging.info(f"book._get_rows_cdocs:docpath: {docpath}")
        doc = self.cdocs.get_doc(docpath)
        if doc is None:
            logging.error(
                f"book._get_rows_cdocs: no content at {docpath} in {self.cdocs.rootname}"
            )
            return []
        logging.info(f"book._get_rows_cdocs:doc: rows: {len(doc)}")
        rows = doc.split("\n")
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

        if self._files.FILES[0:6] != "cdocs:":
            path = f"{self._files.FILES}/{path}"
            section_metadata.FILE = path

            if not os.path.exists(path) and path[0:6] != "cdocs:":
                raise BookfileMistakeException(f"{path} does not exist")

            file_stats = os.stat(path)
            section_metadata.CHAR_COUNT = file_stats.st_size

            with open(path, "r") as contents:
                lines = contents.readlines()
                section = RegularSection(
                    lines,
                    markup=self._markup,  # type: ignore [arg-type]
                    fonts=self._fonts,  # type: ignore [arg-type]
                    document=self._document,
                    metadata=section_metadata,
                )
                section.compile()
        else:
            doc = self.cdocs.get_doc(path)
            logging.info(f"book._append_section: {path} = {doc}")
            if doc:
                lines = doc.split("\n")
                section = RegularSection(
                    lines,
                    markup=self._markup,  # type: ignore [arg-type]
                    fonts=self._fonts,  # type: ignore [arg-type]
                    document=self._document,
                    metadata=section_metadata,
                )
                section.compile()

    def _check_for_inserts(self, line: str) -> None:
        token = "INSERT:"
        insert = line.find(token)
        if insert > 0:
            path = line[insert + len(token) :].strip()
            composer = Composer(self._document)
            doc2 = Document(path)
            composer.append(doc2)

    def _check_for_page_break(self, line: str) -> None:
        token = "PAGEBREAK"
        insert = line.find(token)
        if insert > 0:
            Section.add_page_break(self._document)

    def _check_for_metadata(self, line: str) -> None:
        token = "METADATA"
        insert = line.find(token)
        if insert > 0:
            self.append_metadata()

    def append_metadata(self):
        section = MetadataSection(
            None,
            markup=self._markup,
            fonts=self._fonts,
            document=self._document,
            metadata=self.metadata,
        )
        section.compile()
