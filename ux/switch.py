from rubicon.objc import SEL, ObjCClass, objc_method
from rubicon.objc.runtime import get_class

from .uikit import UIControlEventValueChanged, UISwitch
from .viewcore import ViewCore


def get_switch():
    if get_class('uxSwitch').value is not None:
        return ObjCClass(get_class('uxSwitch'))
    else:
        class uxSwitch(UISwitch):
            @objc_method
            def onPress_(self, obj) -> None:
                if self.interface.action:
                    self.interface.action(obj.interface)
        return uxSwitch

class Switch(ViewCore):
    def __init__(self, **kwargs):
        switchclass = get_switch()
        self.native = switchclass.alloc().init()
        self.native.interface = self
        self.native.addTarget(self.native, action=SEL('onPress:'), forControlEvents=UIControlEventValueChanged)
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
    def value(self) -> bool:
        return self.native.isOn()

    @value.setter
    def value(self, value):
        if isinstance(value, bool):
            self.native.setOn_animated_(value, True)
