from rubicon.objc import CGRect, CGPoint, CGSize, ObjCClass, SEL, objc_method, py_from_ns
from rubicon.objc.runtime import get_class
from .colors import *
from .font import *
from .image import *
from .core import dprint, _in_background, in_background
from .viewcore import ViewCore

from .uikit import (
    UIButton,
    UIColor,
    UIControlEventTouchDown,
    UIControlStateDisabled,
    UIControlStateNormal
)

def get_button():
    if get_class('uxButton').value is not None:
        return ObjCClass(get_class('uxButton'))
    else:
        class uxButton(UIButton):

            @objc_method
            def onPress_(self, obj) -> None:
                if self.interface.action:
                    self.interface.action_handler(obj.interface)

        return uxButton

class Button(ViewCore):
    def __init__(self, **kwargs):
        self.init()
        self.action_handler = None
        btnclass = get_button()
        self.native = btnclass.alloc().init()
        ipath = os.path.join(os.path.dirname(__file__), 'media/images/iob/ios7_circle_filled_32')
        ipath = os.path.join(os.path.dirname(__file__), 'media/images/emj/Artist_Palette')

        self.native.interface = self
        if kwargs.get('title', None):
                self.title = kwargs['title']
                self.native.sizeToFit()
        else:
            self.native.frame = CGRect(CGPoint(10, 10), CGSize(120, 40))

        self.controller = None
        for arg in kwargs:
            if arg == 'action':
                if isinstance(kwargs[arg], Callable):
                    self.action = kwargs[arg]
                else:
                    print('action must be callable')
            elif arg == 'enabled':
                self.enabled = kwargs[arg]
            elif arg == 'font':
                self.font = kwargs[arg]
            elif arg == 'image':
                self.image = kwargs[arg]
            elif arg == 'menu':
                self.menu = kwargs[arg]
            elif arg == 'tint_color':
                self.tint_color = kwargs[arg]
            elif arg == 'title':
                self.title = kwargs[arg]
            elif arg == 'background_image':
                dprint(arg + ' not implemented')
            else:
                if not self.viewattrs(arg, kwargs[arg]):
                    print('invalid button argument: ' + arg)

    def on_action(self, sender):
        _in_background(self.action, sender)

    @property
    def action(self):
        return self.action_handler

    @action.setter
    def action(self, handler):
        if callable(handler):
            self.native.addTarget(self.native, action=SEL('onPress:'), forControlEvents=UIControlEventTouchDown)
            self.action_handler = handler

    @property
    def menu(self):
        return menu.native

    @menu.setter
    def menu(self, menu):
        self.native.menu = menu.native
        if not self.action_handler:
            self.native.showsMenuAsPrimaryAction = True

    @property
    def font(self):
        return (py_from_ns(self.native.font.fontName), py_from_ns(self.native.font.pointSize))

    @font.setter
    def font(self, font):
        self.native.font = Font.named(font)

    @property
    def title(self):
        return self.native.title

    @title.setter
    def title(self, title):
        self.native.setTitle(title, forState=UIControlStateNormal)

    @property
    def image(self):
        return self.native.image

    @image.setter
    def image(self, image):
        self.native.setImage(image, forState=UIControlStateNormal)
        self.native.imagePadding = 20.0

    @property
    def tint_color(self):
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
            dprint(ncolor)
            self.native.setTitleColor(ncolor, forState=UIControlStateNormal)
