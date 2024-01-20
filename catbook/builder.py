from . import Markup
from . import Fonts
from . import Files


class Builder:
    def __init__(self):
        self.markup: Markup = None
        self.fonts: Fonts = None
        self.fonts: Files = None

    def init(self):
        self.markup = Markup()
        self.fonts = Fonts()
        self.files = Files()
