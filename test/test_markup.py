from catbook import Markup


def test_load_no_config():
    markup = Markup()
    assert markup.JUMP == "***"


def test_load_config():
    markup = Markup()
    markup.MARKUP_CONFIG = "test-markup.ini"
    markup.reload()
    assert markup.JUMP == "jump"
