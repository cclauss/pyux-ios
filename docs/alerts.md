ux.Alerts
=========

Using the callback option with alerts and dialogs is highly recommended.
Modal alerts and dialogs without the callback option need to be called
 from a function using the @ux.in_background decorator.

```
@ux.in_background
def alert_modal(sender):
    result = ux.alert('Alert', 'Continue?', 'Ok', 'Maybe', 'No')
    print(result)

def alert_callback(sender):

    def _callback(result):
        print(result)

    ux.alert('Alert', 'Continue?', 'Ok', 'Maybe', 'No', callback=_callback)

```

ux.alert(title[, message, button1, button2, button3, hide_cancel_button=False], callback=None)

- Alert dialog with 1 to 3 buttons
- Button returns integer 1 to 3
- Cancel returns None
- Optional callback sends result to callable

ux.**confirm_dialog**(title, message, callback=None)

- Dialog with OK and Cancel buttons
- OK returns True
- Cancel returns None
- Optional callback sends result to callable

ux.**hud_alert**(message[, icon, duration=1.8])

- HUD Alert
- icon
  - 'success'
  - 'error'
- duration - float

ux.**input_alert**(title[, message, input, ok_button_title, hide_cancel_button=False], callback=None)

- Dialog with text input
- Cancel returns None
- Optional callback sends result to callable

ux.**login_alert**(title[, message, login, password, ok_button_title], callback=None)

- Dialog with login and password inputs
- Cancel returns None
- Optional callback sends result to callable

ux.**password_alert**(title[, message, password, ok_button_title, hide_cancel_button=False], callback=None)

- Dialog with password input
- Cancel returns None
- Optional callback sends result to callable
