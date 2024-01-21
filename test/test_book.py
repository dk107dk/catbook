from catbook import Book
from catbook import Files


def test_two_line_input():
    files = Files()
    files.INPUT = "test/config/one-line-contents.csv"
    files.FILES = "test/config/texts"
    book = Book(files=files, markup=None, fonts=None, document=None)
    cnt = book.create()
    assert cnt == 2
    assert book.files == 1
