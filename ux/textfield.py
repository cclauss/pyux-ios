from rubicon.objc import CGRect, CGPoint, CGSize, ObjCClass, SEL, objc_method, py_from_ns, send_message
from rubicon.objc.runtime import get_class
from ctypes import c_int
from typing import Callable
from .colors import uicolor, uicolor_rgba
from .font import Font
from .viewcore import ViewCore

from .uikit import (
    UIControlEventEditingChanged,
    UITextBorderStyle,
    UITextField,
    UITextInputTraits
)


AUTOCAPITALIZE_NONE = 0
AUTOCAPITALIZE_WORDS = 1
AUTOCAPITALIZE_SENTENCES = 2
AUTOCAPITALIZE_ALL = 3


KEYBOARD_ASCII = 1
KEYBOARD_DECIMAL_PAD = 8
KEYBOARD_DEFAULT = 0
KEYBOARD_EMAIL = 7
KEYBOARD_NAME_PHONE_PAD = 6
KEYBOARD_NUMBERS = 2
KEYBOARD_NUMBER_PAD = 4
KEYBOARD_PHONE_PAD = 5
KEYBOARD_TWITTER = 9
KEYBOARD_URL = 3
KEYBOARD_WEB_SEARCH = 10

def get_textfield():
    if get_class('uxTextField').value is not None:
        return ObjCClass(get_class('uxTextField'))
    else:
        class uxTextField(UITextField, protocols=[UITextInputTraits]):
            @objc_method
            def textFieldShouldBeginEditing_(self, notification) -> bool:
                return self.interface.textfield_should_begin_editing(self.interface)

            @objc_method
            def textFieldDidBeginEditing_(self, notification) -> None:
                self.interface.textfield_did_begin_editing(self.interface)

            @objc_method
            def textFieldDidEndEditing_(self, notification) -> None:
                self.interface.textfield_did_end_editing(self.interface)

            @objc_method
            def textFieldShouldReturn_(self, notification) -> None:
                return self.interface.textfield_should_return(self.interface)

            @objc_method
            def textFieldShouldChange_(self, notification, range, replacement) -> None:
                return self.interface.textfield_should_change(self.interface)

            @objc_method
            def textFieldDidChange_(self, notification) -> None:
                self.interface.textfield_did_change(self.interface)

        return uxTextField

class TextField(ViewCore):
    def __init__(self, **kwargs):
        self.init()
        textclass = get_textfield()
        self.native = textclass.alloc().init()
        self.native.interface = self
        self.native.delegate = self.native
        self.native.frame = CGRect(CGPoint(120, 5), CGSize(240, 50))
        self.native.clearButtonMode = 1
        self.native.borderStyle = UITextBorderStyle.RoundedRect
        self.native.addTarget(
            self.native,
            action=SEL('textFieldDidChange:'),
            forControlEvents=UIControlEventEditingChanged
        )

        for arg in kwargs:
            if arg == 'action':
                if isinstance(kwargs[arg], Callable):
                    self.action = kwargs[arg]
                else:
                    print('action must be callable')
            elif arg == 'alignment':
                self.alignment = kwargs[arg]
            elif arg == 'autocapitalization_type':
                self.autocapitalization_type = kwargs[arg]
            elif arg == 'autocorrection_type':
                self.autocorrection_type = kwargs[arg]
            elif arg == 'bordered':
                self.bordered = kwargs[arg]
            elif arg == 'clear_button_mode':
                self.clear_button_mode = kwargs[arg]
            elif arg == 'enabled':
                self.enabled = kwargs[arg]
            elif arg == 'font':
                self.font = kwargs[arg]
            elif arg == 'keyboard_type':
                self.keyboard_type = kwargs[arg]
            elif arg == 'placeholder':
                self.placeholder = kwargs[arg]
            elif arg == 'secure':
                self.secure = kwargs[arg]
            elif arg == 'spellchecking_type':
                self.spellchecking_type = kwargs[arg]
            elif arg == 'text':
                self.text = kwargs[arg]
            elif arg == 'text_color':
                self.text_color = kwargs[arg]
            else:
                if not self.viewattrs(arg, kwargs[arg]):
                    print('Invalid textfield argument: ' + arg)

    def textfield_should_begin_editing(self, textfield):
        return True

    def textfield_did_begin_editing(self, textfield):
        pass

    def textfield_did_end_editing(self, textfield):
        self.action(self)

    def textfield_should_return(self, textfield):
        return True

    def textfield_should_change(self, textfield):
        return True

    def textfield_did_change(self, textfield):
        pass

    def action(self, sender):
        pass

    def begin_editing(self):
        self.native.becomeFirstResponder()

    def end_editing(self):
        self.native.resignFirstResponder()

    @property
    def alignment(self) -> str:
        return self.native.textAlignment

    @alignment.setter
    def alignment(self, value):
        self.native.textAlignment = value

    @property
    def autocapitalization_type(self) -> str:
        return py_from_ns(self.native.textInputTraits().valueForKey('autocapitalizationType'))

    @autocapitalization_type.setter
    def autocapitalization_type(self, value):
        send_message(
            self.native,
            'setAutocapitalizationType:',
            value,
            restype=None,
            argtypes=[c_int]
        )

    @property
    def autocorrection_type(self) -> str:
        autocorrect = py_from_ns(self.native.textInputTraits().valueForKey('autocorrectionType'))
        if autocorrect == 0:
            return None
        elif autocorrect == 1:
            return False
        elif autocorrect == 2:
            return True

    @autocorrection_type.setter
    def autocorrection_type(self, value):
        autotype = 0
        if type(value) is bool:
            if value:
                autotype = 2
            else:
                autotype = 1
        send_message(
            self.native,
            'setAutocorrectionType:',
            autotype,
            restype=None,
            argtypes=[c_int]
        )

    @property
    def bordered(self) -> bool:
        if self.native.borderStyle > 0:
            return True
        else:
            return False

    @bordered.setter
    def bordered(self, value):
        if value:
            self.native.borderStyle = 3
        else:
            self.native.borderStyle = 0

    @property
    def clear_button_mode(self) -> bool:
        clearmode = self.native.clearButtonMode
        if clearmode == 0:
            return 'never'
        elif clearmode == 1:
            return 'while_editing'
        elif clearmode == 2:
            return 'unless_editing'
        elif clearmode == 3:
            return 'always'

    @clear_button_mode.setter
    def clear_button_mode(self, value):
        if value == 'never':
            self.native.clearButtonMode = 0
        elif value == 'while_editing':
            self.native.clearButtonMode = 1
        elif value == 'unless_editing':
            self.native.clearButtonMode = 2
        elif value == 'always':
            self.native.clearButtonMode = 3

    @property
    def enabled(self) -> bool:
        return self.native.isUserInteractionEnabled()

    @enabled.setter
    def enabled(self, value):
        self.native.userInteractionEnabled = value

    @property
    def font(self):
        return (py_from_ns(self.native.font.fontName), py_from_ns(self.native.font.pointSize))

    @font.setter
    def font(self, font):
        self.native.font = Font.named(font)

    @property
    def keyboard_type(self) -> str:
        kbtype = py_from_ns(self.native.textInputTraits().valueForKey('keyboardType'))
        return kbtype

    @keyboard_type.setter
    def keyboard_type(self, value):
        send_message(
            self.native,
            'setKeyboardType:',
            value,
            restype=None,
            argtypes=[c_int]
        )

    @property
    def placeholder(self) -> str:
        return self.native.placeholder

    @placeholder.setter
    def placeholder(self, value):
        self.native.placeholder = value

    @property
    def secure(self) -> str:
        issecure = py_from_ns(self.native.textInputTraits().valueForKey('secureTextEntry'))
        if issecure == 1:
            return True
        return False

    @secure.setter
    def secure(self, value):
        self.native.setSecureTextEntry_(value)

    @property
    def spellchecking_type(self) -> str:
        spellcheck = py_from_ns(self.native.textInputTraits().valueForKey('spellCheckingType'))
        if spellcheck == 0:
            return None
        elif spellcheck == 1:
            return False
        elif spellcheck == 2:
            return True


    @spellchecking_type.setter
    def spellchecking_type(self, value):
        spellcheck = 0
        if type(value) is bool:
            if value:
                spellcheck = 2
            else:
                spellcheck = 1
        send_message(
            self.native,
            'setSpellCheckingType:',
            spellcheck,
            restype=None,
            argtypes=[c_int]
        )

    @property
    def text(self) -> str:
        return self.native.text

    @text.setter
    def text(self, value):
        self.native.text = value

    @property
    def text_color(self) -> str:
        color = self.native.textColor
        return uicolor_rgba(color)

    @text_color.setter
    def text_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.native.textColor = ncolor
