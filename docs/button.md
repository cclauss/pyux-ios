ux.Button
=========

attributes
----------

Button.**action**

- Callable action when Button is touched

Button.**enabled**

- Boolean

Button.**font**

- Font as tuple (font_name, font_size)

Button.**image**

- ux.Image.named(args)

Button.**menu**

- [ux.Menu](menu.md)
- Primary action if Button.action is None
- Secondary action if Button.action is not None

Button.**tint_color**

- Color for title or image

- Get returns:
  - tuple: (1.0, 0.0, 0.0, 0.5)

- Set as:
  - CSS name: 'blue'
  - hex: '#0000FF'
  - tuple: (0.0, 0.0, 1.0, 0.5)

Button.**title**

- Button title text
