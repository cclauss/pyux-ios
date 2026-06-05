ux.TableViewCell
================

```
# build TableViewCell
def tableview_cell_for_row(self, tableview, section, row):
    cell = ux.TableViewCell(style='subtitle')
    cell.text_label.text = self.tv.data[row][2]
    cell.detail_text_label.text = self.tv.data[row][3]
    cell.detail_text_label.font = ux.Font.named(('Menlo', 14))
    cell.image_view.image = self.cellimage # ux.Image.named('system:wifi.circle') # sfsymbol
    cell.accessory_type = 'detail_button'
    return cell
```
or

```
# return dictionary
def tableview_cell_for_row(self, tableview, section, row):
    return {'title': self.tv.data[row][2],
            'subtitle': '  ' + self.tv.data[row][3],
            'style': 'subtitle',
            'image': self.cellimage,
            'accessory': 'detail_button'
    }
```

Attributes
----------

TableCellView.**style**

- 'default'
- 'subtitle'
- 'value1'
- 'value2'

TableCellView.**text_label**

- text_label.text = 'Python'
- text_label.font = ux.Font.named(('Menlo', 14))

TableCellView.**detail_text_label**

- detail_text_label.text = 'rocks'
- detail_text_label.font = ux.Font.named(('Menlo', 14))

TableCellView.**image_view**

- image_view.image = ux.Image.named('system:wifi.circle') # sfsymbol

TableCellView.**accessory_type**

- 'disclosure_indicator'
- 'detail_disclosure_button'
- 'checkmark'
- 'detail_button'
- 'none'

TableCellView.**content_view**

- ux.View

TableCellView.**selectable**

- Boolean

TableCellView.**selected_background_view**

- ux.View
