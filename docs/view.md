
ux.View
=======

Creating new instance:

- view = ux.View()
- view = ux.View(frame=(0, 0, 580, 620),  background_color='blue')  # with optional properties


Attributes
----------

View.**alpha**

- View's alpha value.
- type: float
- range: 0.0 - 1.0

View.**background_color**

- View's backgroud color.

- Get returns:
  - tuple: (1.0, 0.0, 0.0, 0.5)

- Set as:
  - CSS name: 'blue'
  - hex: '#0000FF'
  - tuple: (0.0, 0.0, 1.0, 0.5)

View.**border_color**

- View's border color.

- Get returns:
  - tuple: (1.0, 0.0, 0.0, 0.5)

- Set as:
  - CSS name: 'blue'
  - hex: '#0000FF'
  - tuple: (0.0, 0.0, 1.0, 0.5)

View.**border_width**

- View's border width.
- type: float or int

View.**bounds**

- View's bounds.
- type: tuple (x, y, width, height)

View.**center**

- Center of view's frame.
- type: tuple (x, y)

View.**corner_radius**

- View’s corner radius.
- type: int or float

View.**flex**

- View's autoresizing behavior.
- type: str

- flags:
  - flexible width: 'W'
  - flexible height: 'H'
  - flexible left margin: 'L'
  - flexible right margin: 'R'
  - flexible top margin: 'T'
  - flexible bottom margin: 'B'

- example: 'WH'

View.**frame**

- View’s position and size
- type: tuple (x, y, width, height)

View.**height**

- View’s frame height.
- type: int or float

View.**left_button_items**

- A iist of ux.ButtonItems that will appear on the left side of the title bar when presented.

- Valid when:
  - Presenting a View instance.
  - Initial View of a ux.NavigationView instance.
  - A View added as a column of a ux.SplitView

View.**name**

- View name that will appear as title when presented.

- Valid when:
  - Presenting a View instance.
  - Initial View of a ux.NavigationView instance.
  - A View added as a column of a ux.SplitView

View.**navigation_view**

- Instance of ux.NavigationView if presented by a NavigationView.

View.**objc_instance**

- Returns the UIKit native component of the view as an objective-c instance.

View.**right_button_items**

- A iist of ux.ButtonItems that will appear on the right side of the title bar when presented.

- Valid when:
  - Presenting a View instance.
  - Initial View of a ux.NavigationView instance.
  - A View added as a column of a ux.SplitView

View.**superview**

- Parent view or None

View.**subviews**

- View’s children
- type: tuple

View.**tag**

- Custom value
- type: Any

View.**width**

- View’s frame width.
- type: int or float

View.**x**

- View’s frame x component.
- type: int or float

View.**y**

- View’s frame y component.
- type: int or float

Methods
-------
View.**add_subview**(view)

- Add a child view
- args:
  - view - ux.View instance


View.**bring_to_front**(view)

- Display view in front of any sibling views
- args:
  - view - ux.View instance

View.**close**()

- Close view

View.**ensure_vc**()

- Ensure view controller. Assigning name, left_button_items or right_button items will do this automatically.

View.**present**(style='sheet', animated=True,
 popover_location=None, hide_title_bar=False,
 title_bar_color=None, title_color=None, orientations=None,
 hide_close_button=False, right_close_button=False)

- Present a view on screen.
- args:
  - style - str
    - 'fullscreen'
    - 'sheet'
    - 'popover'
    - 'fullscreen'
  - animated - boolean
  - popover_location - tuple (x, y)
  - hide_title_bar - boolean
  - title_bar_color - title bar background color
  - title_color - title bar text color
  - orientations - not suppored
  - hide_close_button - boolean
  - right_close_button - boolean - close button on right instead of default left

View.**remove_subview**(view)

- Remove child view
- args:
  - view - ux.View

View.**size_to_fit**()

- Resize view to fit content

View.**tabbar_item**

- Assign title and image for views assigned to ux.TabBar
- tabbar_item.title
- tabbar_item.image

View.**wait_modal**()

- Wait until view disappears
- Overriding **did_close** is recommended as a better option

Events
------
Override event method with custom code.

View.**did_load**()

- View has finished loading

View.**keyboard_will_change**(frame)

- On-screen keyboard will change
- frame - tuple (x, y, height, width)

View.**layout**()

- Use to provide additional layout hints

View.**did_appear**()

- View  has appeared on screen

View.**will_close**()

- View will disappear from screen

View.**did_close**()

- View has disappeared from screen

