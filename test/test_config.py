from catbook import Markup
from catbook import Fonts
from catbook import Files


# ======== MARKUP
def test_load_no_markup_config():
    markup = Markup()
    assert markup.JUMP == "***"


def test_load_markup_config():
    markup = Markup()
    markup.CONFIG = "config/test-markup.ini"
    markup.reload()
    assert markup.JUMP == "jump"


# ======== FONTS
def test_load_no_fonts_config():
    fonts = Fonts()
    assert fonts.QUOTE == "Times New Roman"


def test_load_fonts_config():
    fonts = Fonts()
    fonts.CONFIG = "config/test-fonts.ini"
    fonts.reload()
    assert fonts.QUOTE == "quote"
    assert fonts.BLOCK == "block"
    assert fonts.TITLE == "title"
    assert fonts.BODY == "body"


# ======== FILES
def test_load_no_files_config():
    files = Files()
    assert files.INPUT == "contents.csv"


def test_load_files_config():
    files = Files()
    files.CONFIG = "config/test-files.ini"
    files.reload()
    assert files.INPUT == "input"
    assert files.OUTPUT == "output"
    assert files.FILES == "files"
