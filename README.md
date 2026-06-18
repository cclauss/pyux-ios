## PyUx
  
PyUx is a UI module for iOS written in pure Python.

### Features
- Menu options for Button and ButtonItem controls
- Display styles for Date, DateTime and DatePicker controls
- Callback option for alerts and dialogs helps prevent troublesome background thread issues
- TableView options include long press context menus, pull-down refresh and search 
- NavigationView, SplitView, TabBar and View presentation containers
- Provides **keychain** functions that support bio-metric authentication.
- Native color theme means effortless dark mode. 

---
![Screenshot](assets/uxdocssplit.png?raw=true)

---
### Compatibility
PyUx has been successfully tested with Pythonista, Pyto and Toga.

Scripts are generally compatible with Pythonista scripts. Many existing scripts may only need a simple change to a few import statements.

```
import ux as ui
from ux.dialogs import dialogs
import ux.alerts as console
import ux.keychain as keychain
```

---
### Requirements
The only requirement is [rubicon-objc](https://github.com/beeware/rubicon-objc).

---
### Try it!
Copy the **demo.py** file along with the **examples** and **ux** folders into the iOS Python application of your choice. Launch **demo.py**.

Move the **ux** folder to **site-packages** for general use.

or

Run single line script to install. This will also install rubicon-objc if needed.
```
import requests as r; exec(r.get('https://raw.githubusercontent.com/sbbosco/pyux-ios/main/dist/pyuxinstall.py').content)
```

---
### Acknowledgments

Many thanks to those who made this project possible!

- [Pythonista](https://omz-software.com/pythonista/)
- [Pyto](https://github.com/ColdGrub1384/Pyto)
- [Beeware-Toga](https://github.com/beeware/toga)
- [Pythonista-Webview](https://github.com/mikaelho/pythonista-webview)
- The many Pythonista Forum users over the years.
