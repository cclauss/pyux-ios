import time
from threading import current_thread, main_thread
from rubicon.objc import Block, ObjCInstance, py_from_ns, send_message
from rubicon.objc.runtime import objc_id
from ctypes import c_int

from .core import asyncq, dprint, in_background, on_main_thread, uxviews, waitModal, will_block

from .uikit  import (
    UIAlertAction,
    UIAlertActionStyle,
    UIAlertController,
    UIAlertControllerStyle,
    UIApplication,
)

from .core import topvc, uxviews
dprint('main?', current_thread().name)


class AlertDialog():
    def __init__(self, window, title, message, callback=None):
        self.responses = {}
        self.callback = callback
        self.result = None
        # styles — actionSheet | alert
        self.dialog = UIAlertController.alloc().init()
        self.dialog.title = title
        self.dialog.message = message
        self.dialog.preferredStyle = UIAlertControllerStyle.Alert

        self.populate_dialog()

        window.presentViewController(
            self.dialog,
            animated=False,
            completion=None,
        )

    def populate_dialog(self, dialog):
        pass

    def response(self, value):
        dprint('value', value)
        if not value:
            dprint('KeyboardInterrupt')
            #raise KeyboardInterrupt
            result = None
        elif self.text2:
            uid = py_from_ns(ObjCInstance(self.text1).text)
            pwd = py_from_ns(ObjCInstance(self.text2).text)
            result = (uid, pwd)
        elif self.text1:
            result = str(ObjCInstance(self.text1).text)

        else:
            result = value

        self.set_result(result)
        if self.callback:
            dprint('on result')
            self.callback(result)

    def null_response(self, action: objc_id) -> None:
        self.response(None)

    def true_response(self, action: objc_id) -> None:
        self.response(True)

    def false_response(self, action: objc_id) -> None:
        self.response(False)

    def int_response(self, action: objc_id) -> None:
        title = py_from_ns(ObjCInstance(action).title)
        self.response(self.responses[title])

    def add_int_response_button(self, label, int):
        self.responses[label] = int
        self.dialog.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Default,
                handler=Block(self.int_response, None, objc_id),
            )
        )

    def add_null_response_button(self, label):
        self.dialog.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Default,
                handler=Block(self.null_response, None, objc_id),
            )
        )

    def add_true_response_button(self, label):
        self.dialog.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Default,
                handler=Block(self.true_response, None, objc_id),
            )
        )

    def add_false_response_button(self, label):
        self.dialog.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Cancel,
                handler=Block(self.false_response, None, objc_id),
            )
        )

    def add_textconfig(self, textField: objc_id) -> None:
        if self.input:
            ObjCInstance(textField).text = self.input
        self.text1 = textField

    def add_pwdconfig(self, textField: objc_id) -> None:
        send_message(
            textField,
            'setSecureTextEntry:',
            1,
            restype=None,
            argtypes=[c_int]
        )
        if self.text1:
            self.text2 = textField
        else:
            self.text1 = textField
        if self.pwd:
            ObjCInstance(textField).text = self.pwd

    def add_textfield(self):
        textfield_block=Block(self.add_textconfig, None, objc_id)
        self.dialog.addTextFieldWithConfigurationHandler(textfield_block)

    def add_pwdfield(self):
        textfield_block=Block(self.add_pwdconfig, None, objc_id)
        self.dialog.addTextFieldWithConfigurationHandler(textfield_block)

class Alert(AlertDialog):

    def __init__(self, alert_type, title, message, btns, set_result, callback=None, hide_cancel_button=False):
        self.alert_type = alert_type
        self.hide_cancel_button = hide_cancel_button
        self.btns = btns
        self.text1 = None
        self.text2 = None
        self.input = None
        self.pwd = None
        window = topvc()
        super().__init__(window, title, message, callback=callback)
        dprint('confirm', current_thread().name)

        dprint('btns', btns)
        self.set_result = set_result

        def viewDidLoad(self) -> None:
            dprint('**viewDidLoad**')

    def populate_dialog(self):
        ok_title = 'OK'
        if self.alert_type == 'alert':
            for i, arg in enumerate(self.btns):
                if i > 0 and i < 4:
                    self.add_int_response_button(arg, i)

        elif self.alert_type == 'input_alert':
            for i, arg in enumerate(self.btns):
                if i == 1:
                    self.input = arg
                if i == 2:
                    ok_title = arg

            self.add_textfield()
            self.add_true_response_button(ok_title)

        elif self.alert_type == 'password_alert':
            for i, arg in enumerate(self.btns):
                if i == 1:
                    self.pwd = arg
                if i == 2:
                    ok_title = arg

            self.add_pwdfield()
            self.add_true_response_button(ok_title)

        elif self.alert_type == 'login_alert':
            for i, arg in enumerate(self.btns):
                if i == 1:
                    self.input = arg
                if i == 2:
                    self.pwd = arg
                if i == 3:
                    ok_title = arg

            self.add_textfield()
            self.add_pwdfield()
            self.add_true_response_button(ok_title)

        if not self.hide_cancel_button:
            self.add_false_response_button("Cancel")


class ConfirmDialog(AlertDialog):

    def __init__(self, window, title, message, set_result, callback=None):
        self.text1 = None
        self.text2 = None
        super().__init__(window, title, message, callback=callback)
        dprint('confirm', current_thread().name)
        self.set_result = set_result

        def viewDidLoad(self) -> None:
            dprint('viewDidLoad')

    def populate_dialog(self):
        self.add_true_response_button("OK")
        self.add_false_response_button("Cancel")

def alert(title, *args, hide_cancel_button=False, callback=None):
    dprint('alert started...')
    dprint(args)
    dprint('thread-confirm', current_thread().name)

    if will_block(callback):
        return None

    confirm = 'Delete item?'
    if args:
        message = args[0]
    else:
        message = None
    dprint(args)
    alertwait = waitModal()
    def do_dialog(_self):
        dprint('dialog')
        Alert('alert', title, message, args, alertwait.set_result,
            hide_cancel_button=hide_cancel_button, callback=callback)

    def dlg_thread():
        dprint('dialog', current_thread().name)
        asyncq(do_dialog)

    dlg_thread()

    if not callback:
        alertwait.wait()
        dprint('rs', alertwait.result)
        if alertwait.result == 22:
            return KeyboardInterrupt

        return alertwait.result
    return None

def input_alert(title, *args, hide_cancel_button=False, callback=None):
    if will_block(callback):
        return None

    confirm = 'Delete item?'
    alertwait = waitModal()
    if args:
        message = args[0]

    def do_dialog(_self):
        dprint('dialog')
        Alert('input_alert', title, message, args, alertwait.set_result,
            hide_cancel_button=hide_cancel_button, callback=callback)

    def dlg_thread():
        dprint('dialog', current_thread().name)
        asyncq(do_dialog)

    dlg_thread()

    if not callback:
        alertwait.wait()
        return alertwait.result

    return None

def password_alert(title, *args, hide_cancel_button=False, callback=None):
    if will_block(callback):
        return None

    alertwait = waitModal()
    if args:
        message = args[0]

    def do_dialog(_self):
        dprint('dialog')
        Alert('password_alert', title, message, args, alertwait.set_result,
            hide_cancel_button=hide_cancel_button, callback=callback)

    def dlg_thread():
        dprint('dialog', current_thread().name)
        asyncq(do_dialog)

    dlg_thread()

    if not callback:
        alertwait.wait()
        return alertwait.result

    return None

def login_alert(title, *args, hide_cancel_button=False, callback=None):
    if will_block(callback):
        return None

    alertwait = waitModal()
    if args:
        message = args[0]

    def do_dialog(_self):
        dprint('dialog')
        Alert('login_alert', title, message, args, alertwait.set_result,
            hide_cancel_button=hide_cancel_button, callback=callback)

    def dlg_thread():
        dprint('dialog', current_thread().name)
        asyncq(do_dialog)

    dlg_thread()

    if not callback:
        alertwait.wait()
        return alertwait.result

    return None


def hud_alert(message='', icon='success', duration=1.8):
    from .button import Button
    from .view import View
    from .image import Image

    @in_background
    def waitfor(fn, status, interval=0.1, duration=2):
        dprint('begin', status, interval, duration)
        for n in range(int(duration/interval)):
            time.sleep(interval)
            if status['done']:
                break
            dprint('wait -|-', n, status['done'])
        dprint('done')
        if not status['done']:
            asyncq(fn)

    @on_main_thread
    def _hud_alert(duration):

        status = { 'done': False }

        def button_tapped(sender):
            status['done'] = True
            asyncq(_close)

        def _close(_self):
            hv.close()

        hv = View()
        hv.frame = (0, 0, 580, 620)
        hv.flex = 'WH'
        btn = Button()
        btn.title = '  ' + message
        btn.background_color = (0, 0, 0, 0.7)
        if icon == 'success':
            btn.image = Image.named('system:checkmark')
        else:
            btn.image = Image.named('system:xmark')
        btn.frame = (0, 0, 320, 200)
        btn.center = (hv.width * 0.5, hv.height * 0.3)
        btn.corner_radius = 10
        btn.flex = 'LRTB'
        btn.action = button_tapped
        hv.add_subview(btn)
        ctrl = topvc()
        ctrl.definesPresentationContext = True
        hv.present('popover', hide_title_bar=True)
        waitfor(_close, status, interval=0.1, duration=duration)
        return None
    _hud_alert(duration=duration)


def confirm_dialog(title, message, callback=None):
    if will_block(callback):
        return None

    top = topvc()
    alertwait = waitModal()

    def do_dialog(_self):
        dprint('dialog')
        ConfirmDialog(top, title, message, alertwait.set_result, callback=callback)

    def dlg_thread():
        dprint('dialog', current_thread().name)
        asyncq(do_dialog)

    asyncq(do_dialog)

    if not callback:
        alertwait.wait()
        dprint('rs', alertwait.result)
        return alertwait.result
    return None
