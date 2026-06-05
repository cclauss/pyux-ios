ux.Menu(title, items)
=====================

```
# basic
menu = ux.Menu('Actions', [ 'Add', 'Edit', 'Refresh']

self.tv.right_button_items = [ux.ButtonItem(title='Actions', action=None, menu=menu)]
```

```
# advanced
menu = ux.Menu('Folders',
	[
	    ('Local', menu_handler),
	    ('Cloud', menu_handler),
	    {'title': 'Remote', 'handler': menu_handler, 'image': menuimg, 'xattributes': 1},
	    ('More', [('Sub 1', menu_handler), ('Sub 2', menu_handler)]),
	    ('App Files', menu_handler)   
	]
	
self.tv.right_button_items = [ux.ButtonItem(title='Folders', action=None, menu=menu)]	
```
Menu.**title**

- string

Menu.**items**
- list of types
  
  - tuple (title, handler)
  - dictionary {'title': 'Remote', 'handler': menu_handler, 'image': menuimg, 'xattributes': 1}
  - tuple (title, list) - sub menu

  

