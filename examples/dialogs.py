from datetime import date, datetime, time

import ux
from ux.dialogs import dialogs

textstr = """
This is a modal dialog
"""

"""
Using the callback option with alerts and dialogs is highly recommended.
Modal alerts and dialogs without the callback option need to be called
 from a function using the @ux.in_background decorator.
"""

@ux.in_background
def text_modal(sender):
    print('text modal dialog...')
    print(sender.width)
    result = dialogs.text_dialog(title='Text Dialog', text=textstr)
    print(result)

def text_callback(sender):
    print('text callback...')

    def _callback(result):
        print(result)

    dialogs.text_dialog(title='Text Dialog', text='This is a callback dialog', callback=_callback)

@ux.in_background
def date_modal(sender):
    print('date modal dialog...')
    #result = dialogs.time_dialog(title='Time Dialog')
    result = dialogs.date_dialog(title='Date Dialog')
    print('result', result, type(result))

def date_callback(sender):
    print('date callback...')

    def _callback(result):
        print('result', result)

    # styles auto = 0 wheels = 1 compact = 2 inline = 3
    dialogs.datetime_dialog(title='Date Dialog', style='inline', callback=_callback)

@ux.in_background
def list_modal(sender):
    print('list modal dialog...')
    actions = [[1, 'Add', 'none'], [2, 'Edit', 'checkmark'], [3, 'Delete', 'none']]
    result = dialogs.list_dialog(title='List Dialog', items=actions)
    print('result', result)

def list_callback(sender):
    print('list callback...')
    print('border color', l2.border_color)
    actions = [[1, 'Add', 'none'], [2, 'Edit', 'checkmark'], [3, 'Delete', 'none']]
    
    def _callback(result):
        print('result', result)

    dialogs.list_dialog(title='List Dialog', items=actions, callback=_callback)

accounts = [[1, 'Checking', 'none'], [2, 'Savings', 'none'], [3, 'Cash', 'none']]

today = date.today()
fields = [
    {'key': 'expenseid', 'title': 'expenseid', 'type': 'int', 'hidden': True, 'value': '0'},
    {'key': 'oper', 'title': 'oper', 'type': 'text', 'hidden': True, 'value':'add'},
    {'key': 'cleared', 'title': 'Cleared', 'type': 'switch', 'value': True},
    {'key': 'payee', 'title': 'Payee', 'type': 'text', 'value':'Cateye Cafe'},
    {'key': 'account', 'title': 'Account', 'type': 'list', 'items': accounts, 'id': 3, 'value': 'Cash'},
    {'key': 'date', 'title': 'Date', 'type': 'date', 'valuex': '2019-12-09','value': today, 'format': '%m/%d/%Y'},
    {'key': 'amount', 'title': 'Amount', 'type': 'decimal', 'value': 3.21},
    {'key': 'note', 'title': 'Note', 'type': 'textview', 'value':'ok'}
]

@ux.in_background
def form_modal(sender):
    print('form modal dialog...')
    result = dialogs.form_dialog(title='Form Dialog', fields=fields)
    print('result', result)
    if result:
        print(type(result['date']))
        print('tzinfo', result['date'].tzinfo)

def form_callback(sender):
    print('form callback...')
    
    def _callback(result):
        print('result', result)
    
    dialogs.form_dialog(title='Form Dialog', fields=fields, callback=_callback)
    
    
w, h = ux.get_window_size()    
if w > 600:
    w = 580

view = ux.View()
view.name = 'Run Modal'
view.frame = (0, 0, w, 620)
view.background_color = 'cyan'

t1 = ux.Button(title='Text modal')
t1.frame = (0, 0, 200, 40)
t1.center = (view.width/2, 50)
t1.flex = 'W'
t1.background_color = 'lightgray'
t1.corner_radius = 7
t1.action = text_modal
view.add_subview(t1)

t2 = ux.Button(title='Text callback')
t2.frame = (0, 0, 200, 40)
t2.center = (view.width/2, 120)
t2.flex = 'W'
t2.background_color = 'lightgray'
t2.corner_radius = 7
t2.action = text_callback
view.add_subview(t2)

d1 = ux.Button(title='Date modal')
d1.frame = (0, 0, 200, 40)
d1.center = (view.width/2, 190)
d1.flex = 'W'
d1.background_color = 'lightgray'
d1.corner_radius = 7
d1.action = date_modal
view.add_subview(d1)

d2 = ux.Button(title='Date callback')
d2.frame = (0, 0, 200, 40)
d2.center = (view.width/2, 260)
d2.flex = 'W'
d2.background_color = 'lightgray'
d2.corner_radius = 7
d2.action = date_callback
view.add_subview(d2)

l1 = ux.Button(title='List modal')
l1.frame = (0, 0, 200, 40)
l1.center = (view.width/2, 330)
l1.flex = 'W'
l1.background_color = 'lightgray'
l1.corner_radius = 7
l1.action = list_modal
view.add_subview(l1)

l2 = ux.Button(title='List callback')
l2.frame = (0, 0, 200, 40)
l2.center = (view.width/2, 400)
l2.flex = 'W'
l2.background_color = 'lightgray'
l2.border_width = 2
l2.border_color = 'systemblue'
l2.corner_radius = 7
l2.action = list_callback
view.add_subview(l2)
print('border color', l2.border_color)

f1 = ux.Button(title='Form modal')
f1.frame = (0, 0, 200, 40)
f1.center = (view.width/2, 470)
f1.flex = 'W'
f1.background_color = 'lightgray'
f1.corner_radius = 7
f1.action = form_modal
view.add_subview(f1)

f2 = ux.Button(title='Form callback')
f2.frame = (0, 0, 200, 40)
f2.center = (view.width/2, 540)
f2.flex = 'W'
f2.background_color = 'lightgray'
f2.corner_radius = 7
f2.action = form_callback
view.add_subview(f2)

view.present('sheet', title_bar_color='black', title_color='white', right_close_button=True)


