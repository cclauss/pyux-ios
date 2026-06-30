from rubicon.objc import CGPoint, CGRect, CGSize, py_from_ns

from .colors import uicolor, uicolor_rgba
from .font import Font
from .uikit import NSLineBreakByWordWrapping, UILabel
from .viewcore import ViewCore

ALIGN_LEFT = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = 2
ALIGN_JUSTIFIED = 3
ALIGN_NATURAL = 4

LB_WORD_WRAP = 0
LB_CHAR_WRAP = 1
LB_CLIP = 2
LB_TRUNCATE_HEAD = 3
LB_TRUNCATE_TAIL = 4
LB_TRUNCATE_MIDDLE = 5

class Label(ViewCore):
    def __init__(self, **kwargs):
        self.native = UILabel.new()
        self.native.interface = self
        self.native.lineBreakMode = NSLineBreakByWordWrapping
        self.native.frame = CGRect(CGPoint(20, 60), CGSize(60, 40))
        for arg in kwargs:
            if arg == 'enabled':
                self.enabled = kwargs[arg]
            elif arg == 'font':
                self.font = kwargs[arg]
            elif arg == 'text':
                self.text = kwargs[arg]
            elif arg == 'text_color':
                self.text_color = kwargs[arg]
            elif arg == 'line_break_mode':
                self.line_break_mode = kwargs[arg]
            elif arg == 'number_of_lines':
                self.number_of_lines = kwargs[arg]
            elif arg == 'scales_font':
                self.scales_font = kwargs[arg]
            elif arg == 'min_font_scale':
                self.min_font_scale = kwargs[arg]
            else:
                if not self.viewattrs(arg, kwargs[arg]):
                    print('invalid label argument: ' + arg)

    @property
    def font(self):
        return (py_from_ns(self.native.font.fontName), py_from_ns(self.native.font.pointSize))

    @font.setter
    def font(self, font):
        self.native.font = Font.named(font)

    @property
    def text(self) -> str:
        return self.native.text

    @text.setter
    def text(self, text):
        self.native.text = text

    @property
    def alignment(self):
        return self.native.textAlignment

    @alignment.setter
    def alignment(self, value):
        if value:
            #self.native.textAlignment = NSTextAlignment(value)
            self.native.textAlignment = value

    @property
    def text_color(self):
        color = self.native.textColor
        return uicolor_rgba(color)

    @text_color.setter
    def text_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.native.textColor = ncolor

    @property
    def number_of_lines(self) -> int:
        return self.native.numberOfLines

    @number_of_lines.setter
    def number_of_lines(self, value):
        self.native.numberOfLines = value

    @property
    def line_break_mode(self) -> int:
        return self.native.lineBreakMode

    @line_break_mode.setter
    def line_break_mode(self, value):
        self.native.lineBreakMode = value

    @property
    def scales_font(self) -> int:
        return self.native.adjustsFontSizeToFitWidth

    @scales_font.setter
    def scales_font(self, value):
        self.native.adjustsFontSizeToFitWidth = value

    @property
    def min_font_scale(self) -> int:
        return self.native.minimumScaleFactor

    @min_font_scale.setter
    def min_font_scale(self, value):
        self.native.minimumScaleFactor = value

