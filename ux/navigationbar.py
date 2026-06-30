from ctypes import byref, c_double

from rubicon.objc import CGPoint, CGRect, CGSize, ns_from_py

from .colors import uicolor
from .uikit import (
    NSForegroundColorAttributeName,
    UIColor,
    UINavigationBar,
    UINavigationItem,
)
from .viewcore import ViewCore


class NavigationItem():
    def __init__(self, title='Navbar.Title'):
        self.native = UINavigationItem.alloc().initWithTitle_(title)

    @property
    def left_button_items(self):
        pass

    @left_button_items.setter
    def left_button_items(self, btnitems):
        leftitems = []
        for item in btnitems:
            leftitems.append(item.native)
        self.native.leftBarButtonItems = leftitems

    @property
    def right_button_items(self):
        pass

    @right_button_items.setter
    def right_button_items(self, btnitems):
        rightitems = []
        for item in btnitems:
            rightitems.append(item.native)
        self.native.rightBarButtonItems = rightitems

class NavigationBar(ViewCore):
    def __init__(self, **kwargs):
        self.native = UINavigationBar.alloc().init()
        self.native.interface = self
        self.controller = None
        self.textAttributes = {}
        for arg in kwargs:
            if arg == 'tint_color':
                self.bar_color = kwargs[arg]
            elif arg == 'bar_color':
                self.tint_color = kwargs[arg]
            else:
                if not self.viewattrs(arg, kwargs[arg]):
                    print('invalid button argument: ' + arg)

    @property
    def items(self):
        return self.native.items

    @items.setter
    def items(self, itemlist):
        navitems = []
        for item in itemlist:
            navitems.append(item.native)
        self.native.setItems_animated_(navitems, False)

    @property
    def frame(self):
        return (self.native.frame.origin.x,
                self.native.frame.origin.y,
                self.native.frame.size.width,
                self.native.frame.size.height)

    @frame.setter
    def frame(self, frameset):
        x, y, w, h = frameset
        self.native.frame = CGRect(CGPoint(x,y), CGSize(w, h))

    @property
    def bar_color(self):
        r, g, b, a = c_double(), c_double(), c_double(), c_double()
        color = self.native.barTintColor
        if UIColor(color).getRed(byref(r), green=byref(g),
            blue=byref(b), alpha=byref(a)):
            return (r.value, g.value, b.value, a.value)
        else:
            return None

    @bar_color.setter
    def bar_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.native.barTintColor = ncolor

    @property
    def tint_color(self) -> UIColor:
        r, g, b, a = c_double(), c_double(), c_double(), c_double()
        color = self.native.tintColor
        if UIColor(color).getRed(byref(r), green=byref(g),
            blue=byref(b), alpha=byref(a)):
            return (r.value, g.value, b.value, a.value)
        else:
            return None

    @tint_color.setter
    def tint_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.textAttributes[str(NSForegroundColorAttributeName)] = ncolor
            self.native.setTitleTextAttributes(ns_from_py(self.textAttributes))
