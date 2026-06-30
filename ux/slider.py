from rubicon.objc import SEL, ObjCClass, objc_method
from rubicon.objc.runtime import get_class

from .uikit import (
    UIControlEventTouchCancel,
    UIControlEventTouchUpInside,
    UIControlEventTouchUpOutside,
    UISlider,
)
from .viewcore import ViewCore


def get_slider():
    if get_class('uxSlider').value is not None:
        return ObjCClass(get_class('uxSlider'))
    else:
        class uxSlider(UISlider):
            @objc_method
            def onPress_(self, obj) -> None:
                if self.interface.action:
                    self.interface.action(obj.interface)

            @objc_method
            def onRelease_(self, obj) -> None:
                if self.interface.action:
                    self.interface.action(obj.interface)

        return uxSlider

class Slider(ViewCore):
    def __init__(self, **kwargs):
        uxSlider = get_slider()
        self.native = uxSlider.alloc().init()
        self.native.interface = self
        self.native.addTarget(
            self.native,
            action=SEL("onRelease:"),
            forControlEvents=UIControlEventTouchUpInside
            | UIControlEventTouchUpOutside
            | UIControlEventTouchCancel,
        )

        for arg in kwargs:
            if arg == 'enabled':
                self.enabled = kwargs[arg]
            elif arg == 'action':
                self.action = kwargs[arg]
            elif arg == 'value':
                self.value = kwargs[arg]
            else:
                self.viewattrs(arg, kwargs[arg])

    def action(self, sender):
        pass

    @property
    def enabled(self) -> bool:
        return self.native.isUserInteractionEnabled()

    @enabled.setter
    def enabled(self, enable):
        if isinstance(enable, bool):
            self.native.userInteractionEnabled = enable

    @property
    def value(self):
        return self.native.value

    @value.setter
    def value(self, value):
        self.native.setValue(value, animated=True)

