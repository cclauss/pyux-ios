import time

import ux as ui
import ux.alerts as console
import ux.keychain as keychain
from ux.dialogs import dialogs


@ui.in_background
def prompt_value(sender):
    result = console.input_alert('Keychain data', 'Save to keychain', 'secret')
    if result:
        keychain.set_password('pyux', 'demo', result)
        console.hud_alert(result, icon='success', duration=1.5)
        time.sleep(2)
        keytext = keychain.get_password('pyux', 'demo')
        dialogs.text_dialog(title='From keychain', text=keytext) 

view = ui.View()
view.name = 'Convert UI'
view.frame = (0, 0, 580, 620)
view.background_color = 'cyan'

btn = ui.Button(title='enter value')
btn.frame = (10, 10, 120, 40)
btn.background_color = 'lightgray'
btn.action = prompt_value
view.add_subview(btn)

view.present('sheet', title_bar_color='black', title_color='white')


