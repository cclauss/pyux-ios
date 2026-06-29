import ux
import ux.alerts as console

"""
Using the callback option with alerts and dialogs is highly recommended.
Modal alerts and dialogs without the callback option need to be called
 from a function using the @ux.in_background decorator.
"""
@ux.in_background
def alert_modal(sender):
    print('alert modal dialog...')
    result = console.alert('Alert', 'Continue?', 'Ok', 'Maybe', 'No')
    print(result)
    match result:
        case 1:
            console.hud_alert('Ok', icon='success', duration=1.8)
        case 2:
            console.hud_alert('Maybe', icon='success', duration=1.8)
        case 3:
            console.hud_alert('No', icon='error', duration=1.8)

def alert_callback(sender):
    print('alert callback...')
    
    def _callback(result):
        print(result)
        match result:
            case 1:
                console.hud_alert('Ok', icon='success', duration=1.8)
            case 2:
                console.hud_alert('Maybe', icon='success', duration=1.8)
            case 3:
                console.hud_alert('No', icon='error', duration=1.8)

    console.alert('Alert', 'Continue?', 'Ok', 'Maybe', 'No', callback=_callback)

@ux.in_background
def input_modal(sender):
    print('input modal dialog...')
    print(sender.width)
    result = console.input_alert('Input Alert', 'Enter your name')
    print('result', result, type(result))

def input_callback(sender):
    print('input callback...')
    print(sender.width)
    
    def _callback(result):
        print('result', result)
    
    console.input_alert('Input Alert', 'Enter your name', callback=_callback)

@ux.in_background
def password_modal(sender):
    print('password modal dialog...')
    result = console.password_alert('Password Alert', 'Enter your password')
    print('result', result)

def password_callback(sender):
    print('password callback...')
    print('border color', b6.border_color)
    
    def _callback(result):
        print('result', result)
        
    console.password_alert('Password Alert', 'Enter your password', callback=_callback)

def login_callback(sender):
    print('login callback...')
    
    def _callback(result):
        
        if result:
            print('result', result)
        else:
            print('Canceled')
    
    ux.login_alert('Login', 'Enter your credentials?', callback=_callback)

def confirm_callback(sender):
    print('confirm callback...')
    
    def _callback(result):
        print('result', result)
        if result:
            print('Confirmed')
        else:
            print('Canceled')
    
    ux.confirm_dialog('Delete', 'Are you sure?', callback=_callback)
    
    
w, h = ux.get_window_size()    
if w > 600:
    w = 580

view = ux.View()
view.name = 'Alerts'
view.frame = (0, 0, w, 620)
view.background_color = 'cyan'

b1 = ux.Button(title='Alert Modal')
b1.frame = (0, 0, 200, 40)
b1.center = (view.width/2, 50)
b1.flex = 'W'
b1.background_color = 'lightgray'
b1.corner_radius = 7
b1.action = alert_modal
view.add_subview(b1)

b2 = ux.Button(title='Alert Callback')
b2.frame = (0, 0, 200, 40)
b2.center = (view.width/2, 120)
b2.flex = 'W'
b2.background_color = 'lightgray'
b2.corner_radius = 7
b2.action = alert_callback
view.add_subview(b2)

b3 = ux.Button(title='Input Modal')
b3.frame = (0, 0, 200, 40)
b3.center = (view.width/2, 190)
b3.flex = 'W'
b3.background_color = 'lightgray'
b3.corner_radius = 7
b3.action = input_modal
view.add_subview(b3)

b4 = ux.Button(title='Input callback')
b4.frame = (0, 0, 200, 40)
b4.center = (view.width/2, 260)
b4.flex = 'W'
b4.background_color = 'lightgray'
b4.corner_radius = 7
b4.action = input_callback
view.add_subview(b4)

b5 = ux.Button(title='Password Modal')
b5.frame = (0, 0, 200, 40)
b5.center = (view.width/2, 330)
b5.flex = 'W'
b5.background_color = 'lightgray'
b5.corner_radius = 7
b5.action = password_modal
view.add_subview(b5)

b6 = ux.Button(title='Password callback')
b6.frame = (0, 0, 200, 40)
b6.center = (view.width/2, 400)
b6.flex = 'W'
b6.background_color = 'lightgray'
b6.border_width = 2
b6.border_color = 'systemblue'
b6.corner_radius = 7
b6.action = password_callback
view.add_subview(b6)
print('border color', b6.border_color)

b7 = ux.Button(title='Login')
b7.frame = (0, 0, 200, 40)
b7.center = (view.width/2, 470)
b7.flex = 'W'
b7.background_color = 'lightgray'
b7.corner_radius = 7
b7.action = login_callback
view.add_subview(b7)

b8 = ux.Button(title='Confirm')
b8.frame = (0, 0, 200, 40)
b8.center = (view.width/2, 540)
b8.flex = 'W'
b8.background_color = 'lightgray'
b8.corner_radius = 7
b8.action = confirm_callback
view.add_subview(b8)

view.present('sheet', title_bar_color='black', title_color='white', right_close_button=True)


