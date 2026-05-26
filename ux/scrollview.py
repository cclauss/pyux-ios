import time
from rubicon.objc import NSMakeSize
from .viewcore import ViewCore

from .uikit import (
    UIScrollView
)

class ScrollView(ViewCore):
    def __init__(self, **kwargs):
        self.native = UIScrollView.alloc().init()
        self.native.interface = self
        for arg in kwargs:
            if arg == 'scroll_enabled':
                self.enabled = kwargs[arg]
            else:
                self.viewattrs(arg, kwargs[arg])

        self.controller = None
        self.name = None
        self.right_items = None
        self.navbar = None

        for i in range(1):
            time.sleep(.1)

    @property
    def scroll_enabled(self) -> bool:
        return self.native.scrollEnabled

    @scroll_enabled.setter
    def scroll_enabled(self, enable):
        if isinstance(enable, bool):
            self.native.scrollEnabled = enable

    @property
    def content_size(self):
        return self.native.self.native.contentSize

    @content_size.setter
    def content_size(self, value):
        self.native.contentSize = NSMakeSize(value[0], value[1])
