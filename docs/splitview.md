ux.SplitView
============

```
# primary | secordary
splitview = ux.SplitView('double')  # init with 2 or 'double' creates 2 column SplitView
```

```
# primary | supplementary | secordary
splitview = ux.SplitView(3)  # init with 3 or 'triple' creates 3 column SplitView
```

https://developer.apple.com/documentation/uikit/uisplitviewcontroller?language=objc

Attributes
----------

SplitView.**display_mode**(value)

- 0 or 'auto'
- 1 or 'secondary_only'
- 2 or 'one_beside_secondary'
- 3 or 'one_over_secondary'
- 4 or 'two_beside_secondary'
- 5 or 'two_over_secondary'
- 6 or 'two_displace_secondary'

SplitView.**display_mode_button**

- 0 or 'auto'
- 1 or 'never'
- 2 or 'always'

SplitView.**presents_with_gesture**

- boolean

SplitView.**secondary_only_button**

- boolean

SplitView.**split_behavior**

- 0 = auto
- 1 or 'tile'
- 2 or 'overlay'
- 3 or 'displace'

SplitView.**primary_column_width_fraction**

- float between 0.00 and 1.00

SplitView.**primary_column_width**

- int or float

SplitView.**minimum_primary_column_width**

- int or float

SplitView.**maximum_primary_column_width**

- int or float

SplitView.**supplementary_column_width_fraction**

- float between 0.00 and 1.00

SplitView.**supplementary_column_width**

- int or float

SplitView.**minimum_supplementary_column_width**

- int or float

SplitView.**maximum_supplementary_column_width**

- int or float

Methods
-------

SplitView.**set_view**(view, column)

- view - ux.View
- column
  - 0 or 'primary'
  - 1 or 'supplementary'
  - 2 or 'secordary'
  - 3 or 'compact'


SplitView.**present**()

- 'sheet'
- 'fullscreen'

SplitView.**collapsing_top_column**(proposed)

- override for top column for collapsing top column
- return preferred top column number

SplitView.**single_mode**()

- Set of properties that to help make SplitView behave like NavigationView when rendered in phone.

SplitView.**show_column**(column)

- 0 or 'primary'
- 1 or 'supplementary'
- 2 or 'secordary'

SplitView.**hide_column**(column)

- 0 or 'primary'
- 1 or 'supplementary'
- 2 or 'secordary'

SplitView.**show_primary**()

- Show primary column

SplitView.**show_supplementary**()

- Show supplementary column

SplitView.**show_secordary**()

- Show secordary column()

SplitView.**collapsed**()

- return isCollapsed - read only

SplitView.**close**()

- Close SpiltView instance

