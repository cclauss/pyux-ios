import sys, os, time, shutil

import ux

img = ux.Image.named('system:ellipsis.circle')

view1 = ux.View()
view1.name = 'view1'
view1.background_color = 'cyan'
view1.frame = (0, 0, 300, 600)
view1.flex = 'WH'
view1.tabbar_item.title = 'View-1'
view1.tabbar_item.image = img

view2 = ux.View()
view2.name = 'view2'
view2.background_color = 'blue'
print('blue', view2.background_color)
view2.background_color = '#0000FF'
print('blue', view2.background_color)
view2.background_color = (0.0, 0.0, 1.0, 1.0)
print('blue', view2.background_color)
view2.frame = (0, 0, 300, 600)
view2.flex = 'WH'
view2.tabbar_item.title = 'View-2'
view2.tabbar_item.image = img
btn2 = ux.Button(title='Button')
btn2.background_color = 'black'
btn2.frame = (0, 0, 200, 40)
view2.add_subview(btn2)

view3 = ux.View()
view3.name = 'view3'
view3.background_color = 'gray'
view3.flex = 'WH'
view3.tabbar_item.title = 'View-3'
view3.tabbar_item.image = img

view4 = ux.View()
view4.name = 'view4'
view4.background_color = 'gray'
view4.frame = (0, 0, 300, 600)
view4.flex = 'WH'
view4.tabbar_item.title = 'Exit'
view4.tabbar_item.image = img

tabbar = ux.TabBar()

tabbar.set_views([view1, view2, view3, view4])

def did_appear(sender=None):
    print('did appear')
    tabbar.close()

view4.did_appear = did_appear

print(ux.get_window_traits()['idiom'])

if ux.get_window_traits()['idiom'] == 'phone':
    tabbar.present('fullscreen')
else:
    tabbar.present('sheet')
  



