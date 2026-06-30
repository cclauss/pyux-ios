from .image import Image
from .tableviewcell import TableViewCell
from .view import View

basestring = str

class ListDataSourceList (list):
    def __init__(self, seq, datasource):
        list.__init__(self, seq)
        self.datasource = datasource

    def append(self, item):
        list.append(self, item)
        self.datasource.reload()

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        self.datasource.reload()

    def __delitem__(self, key):
        list.__delitem__(self, key)
        self.datasource.reload()

    def __setslice__(self, i, j, seq):
        list.__setslice__(self, i, j, seq)
        self.datasource.reload()

    def __delslice__(self, i, j):
        list.__delslice__(self, i, j)
        self.datasource.reload()


class ListDataSource (object):
    def __init__(self, items=None):
        self.tableview = None
        self.reload_disabled = False
        self.delete_enabled = True
        self.move_enabled = False

        self.action = None
        self.edit_action = None
        self.accessory_action = None

        self.tapped_accessory_row = -1
        self.selected_row = -1

        if items is not None:
            self.items = items
        else:
            self.items = ListDataSourceList([])
        self.text_color = None
        self.highlight_color = None
        self.font = None
        self.number_of_lines = 1

    def reload(self):
        if self.tableview and not self.reload_disabled:
            pass

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = ListDataSourceList(value, self)
        self.reload()

    def tableview_number_of_sections(self, tv):
        self.tableview = tv
        return 1

    def tableview_number_of_rows(self, tv, section):
        return len(self.items)

    def tableview_can_delete(self, tv, section, row):
        return self.delete_enabled

    def tableview_can_edit(self, tableview, section, row):
        if self.delete_enabled or self.move_enabled:
            return True
        else:
            return False

    def tableview_can_move(self, tv, section, row):
        return self.move_enabled

    def tableview_editing_style(self, tableview, section, row):
        if self.tableview_can_delete(tableview, section, row):
            return 1
        else:
            return 0

    def tableview_accessory_button_tapped(self, tv, section, row):
        self.tapped_accessory_row = row
        if self.accessory_action:
            self.accessory_action(self)

    def tableview_did_select(self, tv, section, row):
        self.selected_row = row
        if self.action:
            self.action(self)

    def tableview_move_row(self, tv, from_section, from_row, to_section, to_row):
        if from_row == to_row:
            return
        moved_item = self.items[from_row]
        self.reload_disabled = True
        del self.items[from_row]
        self.items[to_row:to_row] = [moved_item]
        self.reload_disabled = False
        if self.edit_action:
            self.edit_action(self)

    def tableview_delete(self, tv, section, row):
        self.reload_disabled = True
        del self.items[row]
        self.reload_disabled = False
        tv.interface.delete_rows([row])
        if self.edit_action:
            self.edit_action(self)

    def tableview_cell_for_row(self, tv, section, row):
        item = self.items[row]
        if isinstance(item, str):
            return {'title': str(item), 'subtitle': '', 'style': 'default', 'accessory': 'none'}
        elif isinstance(item, dict):
            return {'title': item.get('title', 'error'),
                    'subtitle': item.get('subtitle', ''),
                    'style': item.get('style', 'default'),
                    'image': item.get('image', None),
                    'accessory_type': item.get('accessory_type', 'none'),
                    'text_color': self.text_color,
                    'font': self.font,
                    'number_of_lines': self.number_of_lines,
                    'highlight_color': self.highlight_color
            }

        item = self.items[row]
        cell = TableViewCell()
        cell.text_label.number_of_lines = self.number_of_lines
        if isinstance(item, dict):
            cell.text_label.text = item.get('title', '')
            img = item.get('image', None)
            if img:
                if isinstance(img, basestring):
                    cell.image_view.image = Image.named(img)
                elif isinstance(img, Image):
                    cell.image_view.image = img
            accessory = item.get('accessory_type', 'none')
            cell.accessory_type = accessory
        else:
            cell.text_label.text = str(item)
        return cell
        if self.text_color:
            cell.text_label.text_color = self.text_color
        if self.highlight_color:
            bg_view = View(background_color=self.highlight_color)
            cell.selected_background_view = bg_view
        if self.font:
            cell.text_label.font = self.font
        return cell
