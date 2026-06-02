ux.TableView
============

Creating new instance:

- table = ux.TableView()
- table = ux.TableView(frame=(0, 0, 580, 620),  background_color='blue')  # with optional properties


Attributes
----------

TableView.**allows_multiple_selection**

- boolean

TableView.**allows_multiple_selection_during_editing**

- boolean

TableView.**allows_selection**

- boolean

TableView.**allows_selection_during_editing**

- boolean

TableView.**editing**

- boolean
- True when table view is in editing mode

TableView.**data**

- built-in datasource items as list

TableView.**data_source**

- Class which implements one or more datasource methods or None

TableView.**delegate**

- Class which implements one or more delegate methods or None

TableView.**refresh_action**

- Callable for pull-down refresh or None

TableView.**row_height**

- row height - int or float

TableView.**search_action**

- Callable for search action or None

TableView.**selected_row**

- list of selected row as tuple [(section, row)]

TableView.**selected_rows**

- list of selected row as tuple [(section, row), (section, row)]

TableView.**separator_color**

- Cell separator color.

- Get returns:
  - tuple: (1.0, 0.0, 0.0, 0.5)

- Set as:
  - CSS name: 'blue'
  - hex: '#0000FF'
  - tuple: (0.0, 0.0, 1.0, 0.5)

Methods
-------

TableView.**begin_refresh**()

- Call at start of refresh action

TableView.**end_refresh**()

- Call at end of refresh action

TableView.**begin_updates**()

- Call at start of direct table data updates

TableView.**end_updates**()

- Call at end of direct table data updates

TableView.**reload**()

- reload table data from datasource

TableView.**reload_data**()

- reload table data from datasource

TableView.**delete_rows**(rows)

- delete rows in list of section-row tuples [(section, row), (section, row)]
- delete list of rows defaults to section 0 [3, 5]

TableView.**insert_rows**

- insert rows in list of section-row tuples [(section, row), (section, row)]
- insert list of rows defaults to section 0 [3, 5]

Datasource methods
------------------

TableView.**tableview_number_of_sections**(tableview)

```
    def tableview_number_of_sections(self, tableview):
        # -- number sections --
        return 1
```

TableView.**tableview_number_of_rows**(tableview, section)

```
    def tableview_number_of_rows(self, tableview, section):
        return len(self.data)
```

TableView.**tableview_cell_for_row**(tableview, section, row)

    def tableview_cell_for_row(self, tableview, section, row):
        item = self.data[row]
        if isinstance(item, str):
            return {'title': str(item), 'subtitle': '', 'style': 'default', 'accessory': 'none'}
        elif isinstance(item, dict):
            return {'title': item.get('title', 'error'),
                    'subtitle': item.get('subtitle', ''),
                    'style': item.get('style', 'default'),
                    'image': item.get('image', None),
                    'accessory_type': item.get('accessory_type', 'none')
            }

TableView.**tableview_title_for_header**(tableview, section)

```
    def tableview_title_for_header(tableview, section):
        # -- section title --
        return ''
```

TableView.**tableview_can_delete**(tableview, section, row)

```
    def tableview_can_delete(self, tableview, section, row):
        return self.delete_enabled
```

TableView.**tableview_can_edit**(tableview, section, row)

```
    def tableview_can_edit(self, tableview, section, row):
        if self.delete_enabled or self.move_enabled:
            return True
        else:
            return False
```

TableView.**tableview_can_move**(tableview, section, row)

```
    def tableview_can_move(self, tableview, section, row):
        return self.move_enabled
```

TableView.**tableview_editing_style**(tableview, section, row)

```
    def tableview_editing_style(self, tableview, section, row):
        if self.tableview_can_delete(tableview, section, row):
            return UITableViewCellEditingStyleDelete
        else:
            return UITableViewCellEditingStyleNone
```

TableView.**tableview_delete**(tableview, section, row)

```
    def tableview_delete(self, tableview, section, row):
        self.begin_updates()
        self.data.pop(row)
        self.delete_rows([(row)])
        self.end_updates()
        if self.edit_action:
            self.edit_action(self)
```

TableView.**tableview_move_row**(tableview, from_section, from_row, to_section, to_row)

```
    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        if from_row == to_row:
            return
        moved_item = self.data[from_row]
        self.begin_updates()
        del self.data[from_row]
        self.data[to_row:to_row] = [moved_item]
        self.end_updates()
        if self.edit_action:
            self.edit_action(self)
        self.reload()
```

TableView.**tableview_height_for_row**(tableview, section, row)

```
    def tableview_height_for_row(self, tableview, section, row):
        return -1
```

Delegate methods
----------------

TableView.**tableview_did_select**(tableview, section, row)

```
    def tableview_did_select(self, tableview, section, row):
        dprint('selelcted: ', row)
        if self.action:
            self.action(self)
```

TableView.**tableview_did_deselect**(tableview, section, row)

```
    def tableview_did_deselect(self, tableview, section, row):
        pass
```

TableView.**tableview_title_for_delete_button**(tableview, section, row)

```
    def tableview_title_for_delete_button(self, tableview, section, row):
        return 'Delete'
```

TableView.**tableview_accessory_button_tapped**(tableview, section, row)

```
    def tableview_accessory_button_tapped(self, tableview, section, row):
        if self.accessory_action:
            self.accessory_action(self)
```

