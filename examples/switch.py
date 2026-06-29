from threading import current_thread

import ux

@ux.in_background
def btnpress(sender):
    print('button clicked')
    
def segaction(sender):
    print('segment selected:', sender.selected_index)
    sender.tint_color = 'yellow'
    sender.enabled = True
    switch.value = not switch.value
    if switch.value:
        txt.begin_editing()
    else:
        txt.end_editing()

@ux.in_background
def switchaction(sender):
    print(current_thread().name)
    print('switch value:', sender.value)
    segment.auto_content_inset = sender.value
    switchactionx(sender)
    
@ux.on_main_thread
def switchactionx(sender):
    print(current_thread().name)
    print('switch value main:', sender.value)
    
def layout():
    print('-- layout --')
    segment.center = (myview.width/2, 20)
    print(myview.frame)
    
segment = ux.SegmentedControl()
segment.segments = ['One', 'Two', 'Three']        
segment.selected_index = 0
segment.background_color = 'black'
segment.font = ('Menlo', 18)
segment.tint_color = 'white'
segment.highlight_color = 'blue'
segment.action = segaction

lbl = ux.Label(frame=(20, 70, 120, 40), text_color='green', background_color='black')
lbl.text = 'Hello Python!'
lbl.number_of_lines = 1
lbl.scales_font = False
lbl.line_break_mode = ux.LB_WORD_WRAP
lbl.alignment = ux.ALIGN_CENTER

btn = ux.Button(frame=(150, 70, 150, 40),
    tint_color=(0.0392, 0.5176, 1.0, 1.0), background_color='black')
btn.title = 'Click'
btn.font = ('Menlo', 18)
btn.image = ux.Image.named('system:cloud')
btn.action = btnpress

switch = ux.Switch(action=switchaction)
switch.frame = (150, 140, 100, 40)

txt = ux.TextView()
txt.frame = (20, 190, 280, 240)
txt.text = 'hello textview'
txt.text_color = 'yellow'
txt.background_color = 'gray'
txt.bordered = False
txt.alignment = ux.ALIGN_LEFT
txt.editable = True
txt.font = ('Menlo', 24)
txt.selectable = True

myview = ux.View(background_color='cyan')
myview.name = 'SegmentedControl - Switch'
myview.frame = (0, 0, 520, 640)
myview.add_subview(segment)
myview.add_subview(lbl)
myview.add_subview(btn)
myview.add_subview(switch)
myview.add_subview(txt)
myview.layout = layout

if __name__ == '__main__':
    nav = ux.NavigationView(myview)
    nav.present('sheet')
