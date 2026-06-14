ux.ButtonItem
=============

ux.ButtonItem**(title=None, image=None, action=None, menu=None, enabled=True, tint_color=None)**

Assign to View.left_button_items or View.right_button_items to create toolbar for presented viewa.

attributes
----------

ButtonItem.**action**

- Callable action when ButtonItem is touched

ButtonItem.**enabled**

- Boolean

ButtonItem.**image**

- ux.Image.named(args)
- Set image or title, but not both.

ButtonItem.**menu**

- [ux.Menu](menu.md)
- Primary action if ButtonItem.action is None
- Secondary action if ButtonItem.action is not None

ButtonItem.**tint_color**

- Color for title or image

- Get returns:
  - tuple: (1.0, 0.0, 0.0, 0.5)

- Set as:
  - CSS name: 'blue'
  - hex: '#0000FF'
  - tuple: (0.0, 0.0, 1.0, 0.5)

ButtonItem.**title**

- Set image or title, but not both.
