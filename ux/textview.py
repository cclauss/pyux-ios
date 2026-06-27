from rubicon.objc import CGRect, CGPoint, CGSize, ObjCClass, objc_method, py_from_ns, send_message
from rubicon.objc.runtime import get_class
from ctypes import c_int
from .core import asyncq
from .colors import uicolor, uicolor_rgba
from .font import Font
from .viewcore import ViewCore

from .uikit import (
    UITextInputTraits,
    UITextView
)


def get_textview():
    if get_class('uxTextView').value is not None:
        return ObjCClass(get_class('uxTextView'))
    else:

        class uxTextView(UITextView, protocols=[UITextInputTraits]):
            @objc_method
            def XpointInside_withEvent_(self, point: CGPoint, event) -> bool:
                within_x = point.x > 0 and point.x < self.frame.size.width
                within_y = point.y > 0 and point.y < self.frame.size.height
                in_view = within_x and within_y
                if not in_view:
                    self.resignFirstResponder()
                return in_view

            @objc_method
            def textViewShouldBeginEditing_(self, notification) -> bool:
                return self.interface.textview_should_begin_editing(self.interface)

            @objc_method
            def textViewDidBeginEditing_(self, notification) -> None:
                self.interface.textview_did_begin_editing(self.interface)

            @objc_method
            def textViewDidEndEditing_(self, notification) -> None:
                self.interface.textview_did_end_editing(self.interface)

            @objc_method
            def textViewShouldReturn_(self, notification) -> None:
                return self.interface.textview_should_return(self.interface)

            @objc_method
            def textViewShouldChange_(self, notification, range, replacement) -> None:
                return self.interface.textview_should_change(self.interface)

            @objc_method
            def textViewDidChange_(self, notification) -> None:
                self.interface.textview_did_change(self.interface)

        return uxTextView

class TextView(ViewCore):
    def __init__(self, **kwargs):
        self.init()
        textvclass = get_textview()
        self.native = textvclass.alloc().initWithFrame(CGRect(CGPoint(0, 100), CGSize(100, 100)), textContainer=None)
        self.native.interface = self
        self.native.delegate = self.native
        self._auto_content_inset = True

        for arg in kwargs:
            if arg == 'alignment':
                self.alignment = kwargs[arg]
            elif arg == 'autocapitalization_type':
                self.autocapitalization_type = kwargs[arg]
            elif arg == 'autocorrection_type':
                self.autocorrection_type = kwargs[arg]
            elif arg == 'auto_content_inset':
                self.auto_content_inset = kwargs[arg]
            elif arg == 'editable':
                self.editable = kwargs[arg]
            elif arg == 'font':
                self.font = kwargs[arg]
            elif arg == 'keyboard_type':
                self.keyboard_type = kwargs[arg]
            elif arg == 'selectable':
                self.selectable = kwargs[arg]
            elif arg == 'selected_range':
                self.selected_range = kwargs[arg]
            elif arg == 'spellchecking_type':
                self.spellchecking_type = kwargs[arg]
            elif arg == 'text':
                self.text = kwargs[arg]
            elif arg == 'text_color':
                self.text_color = kwargs[arg]
            else:
                if not self.viewattrs(arg, kwargs[arg]):
                    print('Invalid textfield argument: ' + arg)

    def keyboard_will_change(self, kbframe):
        kbx, kby, kbw, kbh = kbframe
        #print('-kbh-', kbh)
        return

    def update_kb_height(self, h):
        #print( '-- update keyboard --', h)
        if h < 0:
            h = 0
        self.content_inset = (0, 0, h, 0)

    @property
    def content_inset(self):
        return self.native.isEditing()

    @content_inset.setter
    def content_inset(self, value):
        t, left, b, r = value
        def _async(_self):
            contentInset = self.native.contentInset
            contentInset.bottom = b
            scrollInsets = self.native.scrollIndicatorInsets
            scrollInsets.bottom = b
            self.native.contentInset = contentInset
            self.native.scrollIndicatorInsets = scrollInsets
        asyncq(_async)

    def textview_should_begin_editing(self, textview):
        return True

    def textview_did_begin_editing(self, textview):
        self.native.scrollRectToVisible(textview.native.frame, animated=True)

    def textview_did_end_editing(self, textview):
        pass

    def textview_should_return(self, textview):
        return True

    def textview_should_change(self, textview):
        return True

    def textview_did_change(self, textview):
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
        autocorrect = self.native.autocorrectionType
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
    def auto_content_inset(self) -> bool:
        return self._auto_content_inset

    @auto_content_inset.setter
    def auto_content_inset(self, value):
        self._auto_content_inset = value

    @property
    def editable(self) -> bool:
        return self.native.isEditable()

    @editable.setter
    def editable(self, value):
        self.native.editable = value

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
    def selectable(self) -> bool:
        return self.native.isSelectable()

    @selectable.setter
    def selectable(self, value):
        self.native.selectable = value

    @property
    def selected_range(self) -> bool:
        range = self.native.selectedRange
        return (range.location, range.location + range.length)

    @selected_range.setter
    def selected_range(self, value):
        self.native.selectedRange = value

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
