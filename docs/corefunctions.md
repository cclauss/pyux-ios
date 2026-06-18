Core functions
==============

ux.**asyncq**(fn)

- Run function asynchronously on main UI thread

```
def async_code(_self):
    print("async queue!")

ux.asyncq(async_code)
```
same as:

```
@ux.on_main_thread
def async_code():
    print("async queue!")
```

ux.**options**

```
{
    'debuglevel' 0,
    'toga' False
}
```

ux.**dprint**(*args)

- Optional printing based on ux.options['degbublevel']

```
def dprint(*args):
    if options['debuglevel'] > 0:
        print('debug: ', args)
```
ux.**py3kit**

- True if 'Pythonista3.app' in sys.executable

ux.**pyto**

- True if 'Pyto.app' in sys.executable

ux.**ios_version**()

- return iOS version as string

ux.**ios_version_info**()

- return iOS version as tuple

ux.**get_screen_size**()

- return screen size as tuple (width, height)

ux.**get_window_size**()

- return window size as tuple (width, height)

ux.**get_window_traits**()

- return window traits as dictionary

```
    { 'idiom': 'phone',          # phone, pad
      'style': 'dark',           # light, dark
      'hsize_class': 'compact',  # compact, normal
      'vsize_class': 'normal'    # compact, normal
    }
```
ux.**rootvc**()

- return root ViewController

ux.**topvc()**

- return top ViewController

ux.**in_background**(fn)

- Use function decorator to run function in background thread

```
@ux.in_background
def background_code():
    print('background thread')
```

ux.**on_main_thread**(fn)

- Use function decorator to run function on main UI thread

```
@ux.on_main_thread
def update_ui():
    print('main ui thread')
```

ux.**convert_point**(point=(0, 0), from_view=None, to_view=None)

- Convert a point from one view’s coordinate system to another. If from_view or to_view is None, the screen coordinate system is used.

ux.**convert_rect**(rect=(0, 0, 0, 0), from_view=None, to_view=None)

- Convert a rectangle from one view’s coordinate system to another. If from_view or to_view is None, the screen coordinate system is used.

ux.**animate**(fn, duration)

- Animate view attribute changes
