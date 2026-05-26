from rubicon.objc import py_from_ns
from .viewcore import ViewCore

from .uikit import (
    UIActivityIndicatorView
)

ACTIVITY_INDICATOR_STYLE_WHITE = 100
ACTIVITY_INDICATOR_STYLE_WHITE_LARGE = 101

class ActivityIndicator(ViewCore):
    def __init__(self, **kwargs):
        self.native = UIActivityIndicatorView.alloc().initWithActivityIndicatorStyle(ACTIVITY_INDICATOR_STYLE_WHITE_LARGE)
        self.native.interface = self
        for arg in kwargs:
            if arg == 'style':
                self.style = kwargs[arg]
            elif arg == 'hides_when_stopped':
                self.hides_when_stopped = kwargs[arg]
            else:
                if not self.viewattrs(arg, kwargs[arg]):
                    print('invalid label argument: ' + arg)

    @property
    def style(self):
        return (py_from_ns(self.native.font.fontName), py_from_ns(self.native.font.pointSize))

    @style.setter
    def style(self, value):
        self.native.style = value

    @property
    def hides_when_stopped(self):
        return self.native.text

    @hides_when_stopped.setter
    def hides_when_stopped(self, value):
        self.native.hidesWhenStopped = value

    def start(self):
        self.native.startAnimating()

    def stop(self):
        self.native.stopAnimating()


