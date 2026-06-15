ux.TabBar
=========

Methods
-------

TabBar.**set_views**([view1, view2, view3, view4])

- List of ux.View instances
- Set **tabbar_item** attributes for each view
  - view.tabbar_item.title = 'View-1'
  - view.tabbar_item.image = ux.Image.named('system:wifi.circle') # sfsymbol

TabBar.**present**(style='sheet')

- 'sheet'
- 'fullscreen'

TabBar.**close**()

- Close TabBar

