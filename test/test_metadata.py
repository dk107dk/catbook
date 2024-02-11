from catbook import Book
from catbook import Files
from catbook import Markup
from catbook import Fonts
from docx import Document


def test_coda_author():
    files = Files()
    files.INPUT = "test/config/coda.bookfile"
    files.FILES = "test/config/texts"
    book = Book(files=files, markup=Markup(), fonts=Fonts(), document=Document())
    cnt = book.create()
    assert cnt == 3
    assert book.files == 1
    meta = book.metadata
    print(f"\nmeta: {meta}")
    assert meta.AUTHOR == "John Doe"
