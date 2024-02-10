from catbook import Book
from catbook import Files


def test_two_line_input_csv():
    files = Files()
    files.INPUT = "test/config/one-line-contents.csv"
    files.FILES = "test/config/texts"
    book = Book(files=files, markup=None, fonts=None, document=None)
    cnt = book.create()
    assert cnt == 2
    assert book.files == 1


def test_two_line_input_txt():
    files = Files()
    files.INPUT = "test/config/one-line-contents.txt"
    files.FILES = "test/config/texts"
    book = Book(files=files, markup=None, fonts=None, document=None)
    cnt = book.create()
    assert cnt == 2
    assert book.files == 1


def test_two_line_input_bookfile():
    files = Files()
    files.INPUT = "test/config/one-line-contents.bookfile"
    files.FILES = "test/config/texts"
    book = Book(files=files, markup=None, fonts=None, document=None)
    cnt = book.create()
    assert cnt == 2
    assert book.files == 1


def test_both_two_line_input_bookfiles_are_equal():
    txtfiles = Files()
    txtfiles.INPUT = "test/config/one-line-contents.txt"
    txtfiles.FILES = "test/config/texts"
    book = Book(files=txtfiles, markup=None, fonts=None, document=None)
    txt = book._get_rows()

    csvfiles = Files()
    csvfiles.INPUT = "test/config/one-line-contents.csv"
    csvfiles.FILES = "test/config/texts"
    book = Book(files=csvfiles, markup=None, fonts=None, document=None)
    csv = book._get_rows()

    assert txt == csv


def test_two_line_input_bookfile_section_count():
    files = Files()
    files.INPUT = "test/config/one-line-contents.bookfile"
    files.FILES = "test/config/texts"
    book = Book(files=files, markup=None, fonts=None, document=None)
    book.create()
    metadata = book.metadata
    assert metadata.count == 1
    print(f"metadata: {metadata}")
    assert metadata.SECTIONS[0] is not None
    assert metadata.SECTIONS[0].NAME == "fish"


def test_coda_bookfile():
    files = Files()
    files.INPUT = "test/config/coda.bookfile"
    files.FILES = "test/config/texts"
    book = Book(files=files, markup=None, fonts=None, document=None)
    cnt = book.create()
    assert cnt == 1
    assert book.files == 1
