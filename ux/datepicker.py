from rubicon.objc import ObjCClass, SEL, ns_from_py, objc_method
from rubicon.objc.runtime import get_class
from .core import asyncq, options
from .viewcore import ViewCore
from .foundation import NSDateFormatter
from .uikit import (
    UIControlEventValueChanged,
    UIDatePicker
)
from threading import current_thread, main_thread
import time

def get_datefield():
    if get_class('uxDatePicker').value is not None:
        return ObjCClass(get_class('uxDatePicker'))
    else:
        class uxDatePicker(UIDatePicker):
            @objc_method
            def dateChanged_(self, notification) -> None:
                if self.interface.action:
                    self.interface.action(self.interface)

        return uxDatePicker

class DatePicker(ViewCore):
    def __init__(self, mode=1, style=3):
        self.init()
        self.native = None
        if mode == 'time':
            mode = 0
        elif mode == 'date':
            mode = 1
        elif mode == 'datetime':
            mode = 2
        elif mode == 'duration':
            mode = 3
        else:
            pass

        if style == 'auto':
            style = 0
        elif style == 'wheels':
            style = 1
        elif style == 'compact':
            style = 2
        elif style == 'inline':
            style = 3
        else:
            pass

        #@on_main_thread
        def _init(_self):
            self.native = dateclass.new()
            self.tag = 0
            self.native.interface = self
            self.native.datePickerMode = mode # .time = 0 .date = 1 .datetime = 2
            self.native.preferredDatePickerStyle = style # .auto = 0 .wheels = 1 .compact = 2 .inline = 3

            self.native.addTarget(
                self.native,
                action=SEL('dateChanged:'),
                forControlEvents=UIControlEventValueChanged
            )
            self.native.retain()

        dateclass = get_datefield()

        if current_thread().name.startswith('Thread') \
            or (current_thread() == main_thread() and not options['toga']):

            asyncq(_init)
            count = 0
            while not self.native:
                time.sleep(.02)
                count += 1
                if count == 5:
                    break
        else:
            _init(None)

    def action(self, datepicker):
        pass

    @property
    def enabled(self) -> bool:
        return self.native.isUserInteractionEnabled()

    @enabled.setter
    def enabled(self, enable):
        if isinstance(enable, bool):
            self.native.userInteractionEnabled = enable

    @property
    def date(self):
        return self.native.date

    @date.setter
    def date(self, value):
        formatter = NSDateFormatter.alloc().init()
        formatter.dateFormat = "yyyy-MM-dd"
        datestr = ns_from_py(value)
        self.native.date = formatter.dateFromString(datestr)
