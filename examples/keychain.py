import ux
import ux.alerts as console
import ux.keychain as keychain

def prompt_value1(sender):

    def _callback(result):
        if result:
            keychain.delete_password('pyux', 'demo1')
            keychain.set_password('pyux', 'demo1', result)
            console.hud_alert(result, icon='success', duration=1.5)

    console.input_alert('Keychain data', 'Save to keychain', 'secret1a', callback=_callback)


def prompt_value2(sender):

    def _callback(result):
        if result:
            keychain.delete_password('pyux', 'demo2')
            keychain.set_password('pyux', 'demo2', result, authentication=None)
            console.hud_alert(result, icon='success', duration=1.5)

    console.input_alert('Keychain data', 'Save to keychain', 'secret2a', callback=_callback)

def prompt_biometric1(sender):
    """
    FaceID only available if NSFaceIDUsageDescription key is found in application Info.plist file.
    Pythonista = True
    Pyto = False
    """

    def _callback(result):

        if result:
            # Delete password if switching to or from biometric.
            keychain.delete_password('pyux', 'demo1')
            keychain.set_password('pyux', 'demo1', result, authentication='biometric')
            console.hud_alert(result, icon='success', duration=1.5)

    console.input_alert('Keychain data', 'Save to keychain', 'secret1b', callback=_callback)

def prompt_biometric2(sender):

    def _callback(result):
        if result:
            keychain.delete_password('pyux', 'demo2')
            keychain.set_password('pyux', 'demo2', result, authentication='biometric')
            console.hud_alert(result, icon='success', duration=1.5)

    console.input_alert('Keychain data', 'Save to keychain', 'secret2b', callback=_callback)

def get_values(sender):
    """
    The context option will allow fetching multiple protected values with one authentication.
    The context is valid for 10 seconds.
    """
    context = keychain.new_context()
    keytext1 = keychain.get_password('pyux', 'demo1', context=context)
    keytext2 = keychain.get_password('pyux', 'demo2', context=context)
    console.hud_alert(str(keytext1) + ' : ' + str(keytext2), icon='success', duration=1.5)


w, h = ux.get_window_size()
if w > 600:
    w = 580

view = ux.View()
view.name = 'Keychain'
view.frame = (0, 0, w, 620)
view.background_color = 'cyan'

b1 = ux.Button(title='Save value 1')
#t1 = ux.Button()
#b1.title = '   dialog   '
#b1.name = 'btnpopup'
b1.frame = (0, 0, 200, 40)
b1.center = (view.width/2, 50)
b1.flex = 'W'
b1.background_color = 'lightgray'
b1.corner_radius = 7
b1.action = prompt_value1
view.add_subview(b1)

b2 = ux.Button(title='Save value 2')
#b2.name = 'btnpopup'
b2.frame = (0, 0, 200, 40)
b2.center = (view.width/2, 120)
b2.flex = 'W'
b2.background_color = 'lightgray'
b2.corner_radius = 7
b2.action = prompt_value2
view.add_subview(b2)

b3 = ux.Button(title='Save biometric 1')
#b3.name = 'btnpopup'
b3.frame = (0, 0, 200, 40)
b3.center = (view.width/2, 190)
b3.flex = 'W'
b3.background_color = 'lightgray'
b3.corner_radius = 7
b3.action = prompt_biometric1
view.add_subview(b3)

b4 = ux.Button(title='Save biometric 2')
#b4.name = 'btnpopup'
b4.frame = (0, 0, 200, 40)
b4.center = (view.width/2, 260)
b4.flex = 'W'
b4.background_color = 'lightgray'
b4.corner_radius = 7
b4.action = prompt_biometric2
view.add_subview(b4)

b5 = ux.Button(title='Get values 1 & 2')
b5.frame = (0, 0, 200, 40)
b5.center = (view.width/2, 330)
b5.flex = 'W'
b5.background_color = 'lightgray'
b5.corner_radius = 7
b5.action = get_values
view.add_subview(b5)

view.present('sheet', title_bar_color='black', title_color='white', right_close_button=True)
