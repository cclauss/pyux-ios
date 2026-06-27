from rubicon.objc import ObjCClass, objc_method
from rubicon.objc.runtime import get_class
from .core import dprint
from .viewcore import ViewCore

from .uikit import UIView

def get_view():
    if get_class('uxView').value is not None:
        return ObjCClass(get_class('uxView'))
    else:
        class uxView(UIView):

            @objc_method
            def isFlipped(self) -> bool:
                # Default Cocoa coordinate frame is around the wrong way.
                return True

            @objc_method
            def display(self) -> None:
                self.layer.setNeedsDisplay_(True)
                self.layer.displayIfNeeded()

        return uxView


class View(ViewCore):

    def __init__(self, **kwargs):
        self.init()
        dprint('view init')
        viewclass = get_view()
        self.native = viewclass.alloc().init()
        self.native.interface = self
        for arg in kwargs:
            if self.viewattrs(arg, kwargs[arg]):
                continue

        self.controller = None
        self.name = None
        self.right_items = False
        self.navbar = None

    @property
    def insets(self):
        return self.native.safeAreaInsets

