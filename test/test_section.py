from catbook import Section
from catbook import Markup
from catbook import Fonts
from docx import Document


def test_last_line():
    section = Section([], None, None, None)

    assert section._last_line(["", "", ""], 2)
    assert section._last_line(["a", "", ""], 0)
    assert section._last_line(["a", "b", "c"], 2)
    assert not section._last_line(["a", "b", "c"], 0)
    assert not section._last_line(["", "", "c"], 0)


def test_handle_block():
    fonts = Fonts()
    markup = Markup()
    markup.BLOCK = "|"
    document = Document()
    section = Section(lines=[], markup=markup, fonts=fonts, document=document)

    assert section._handle_block("| a block line", 1, 100)
    assert section._handle_block("|another block line", 2, 100)
    assert len(section._block) == 2
    assert not section._handle_block("a non-block line", 1, 100)
    assert section._block is None


def test_handle_quote():
    fonts = Fonts()
    markup = Markup()
    markup.QUOTED_LINE = '"'
    document = Document()
    section = Section(lines=[], markup=markup, fonts=fonts, document=document)

    assert section._handle_quote('"a quote line', 1, 100)
    assert len(section._quote) == 1
    assert not section._handle_quote("a non-quote line", 2, 100)
    assert section._quote is None
