from catbook import Markup
from catbook import Fonts
from catbook import Files
from catbook import Misc


# ======== MARKUP
def test_load_no_markup_config():
    markup = Markup()
    assert markup.JUMP == "***"


def test_load_markup_config():
    markup = Markup()
    markup.CONFIG = "config/test-markup.ini"
    markup.reload()
    assert markup.JUMP == "jump"


def test_is_block_or_quote():
    markup = Markup()
    markup.BLOCK = "|"
    markup.QUOTE = '"'

    assert not markup._is_quote("", 5, 10)
    assert not markup._is_quote("this is a line", 5, 10)
    assert markup._is_quote('"this is a line', 5, 10)

    assert not markup._is_block("", 5, 10)
    assert not markup._is_block("this is a line", 5, 10)
    assert markup._is_block("|this is a line", 5, 10)
    assert markup._is_block("||this is a line", 5, 10) is None


# ======== MISC


def test_misc():
    misc = Misc()
    misc.CONFIG = "test/config/misc.ini"
    misc.reload()

    vals = [_ for _ in misc.get_numbered("email")]
    print(f"vals: {vals}")
    assert len(vals) == 3
    assert vals[0] == "test1@test.com"


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


def test_load_files_config():
    files = Files()
    files.CONFIG = "config/test-files.ini"
    files.reload()
    assert files.INPUT == "input"
    assert files.OUTPUT == "output"
    assert files.FILES == "files"
