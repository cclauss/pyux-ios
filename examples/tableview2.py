import json

import ux

with open('uxdocs.json') as in_file:
    uxdocs = json.load(in_file)

class TableView2():
    
    def __init__(self):
        self.tv = ux.TableView()
        self.tv.name = 'TableView'
        self.tv.data = []
        self.tv.allows_multiple_selection = True
        self.tv.data_source = self.tv.delegate = self
        self.menuitems1 = [
                        ('Refresh', self.menu_handler),
                        ('Add', self.menu_handler),
                        ('Edit', self.menu_handler)
                    ]
        self.menuitems2 = [
                        ('Refresh', self.menu_handler),
                        ('Add', self.menu_handler),
                        ('Done', self.menu_handler)
                    ]
        self.btnimage = ux.Image.named('system:ellipsis.circle') # sfsymbol
        self.cellimage = ux.Image.named('system:wifi.circle') # sfsymbol
        menu = ux.Menu('Actions', self.menuitems1)
        self.btnaction = ux.ButtonItem(image=self.btnimage, action=None, menu=menu)
        self.tv.right_button_items = [self.btnaction]
        self.tv.separator_color = 'cyan'
        self.tv.present('sheet')
        self.refresh()
        
    def refresh(self):
        dsitems = []
        classes = uxdocs['classes']
        for i, key in enumerate(classes.keys()):
            dsitems.append((i, key, classes[key]['name'], classes[key]['constructor']))
        self.tv.data = dsitems
        self.tv.reload()

    def tableview_cell_for_row(self, tableview, section, row):
        if row == 2:
            cell = ux.TableViewCell(style='subtitle')
            cell.text_label.text = self.tv.data[row][2]
            cell.detail_text_label.text = self.tv.data[row][3]
            cell.detail_text_label.font = ux.Font.named(('Menlo', 14))
            cell.image_view.image = self.cellimage
            cell.accessory_type = 'detail_button'
            return cell
        else:
            return {'title': self.tv.data[row][2],
                    'subtitle': '  ' + self.tv.data[row][3],
                    'style': 'subtitle', 
                    'accessory': 'detail_button'
            }

    def tableview_did_select(self, tableview, section, row):
        print('did select')
        print(self.tv.data[row])

    def tableview_accessory_button_tapped(self, tableview, section, row):
        print('accessory', row)
        self.tv.selected_rows = [(0, 4), (0, 6)]
        print(self.tv.selected_rows)

    def tableview_title_for_delete_button(self, tableview, section, row):
        return 'Delete it?'
        
    def tableview_delete(self, tableview, section, row):
        print('delete:', row)
        self.tv.begin_updates()
        self.tv.data.pop(row)
        self.tv.delete_rows([(0, row)])
        self.tv.end_updates()

    def menu_handler(self, sender):
        print(sender.title)
        action = sender.title
        if action == 'Refresh':
            self.refresh()
        elif action == 'Edit' or action == 'Done':
            self.tv.editing = not self.tv.editing
            if self.tv.editing:
                menu = ux.Menu('Actions', self.menuitems2)
            else:
                menu = ux.Menu('Actions', self.menuitems1)
            self.btnaction.menu = menu
        elif action == 'Add':
            self.tv.begin_updates()
            self.tv.data.insert(3, [3, 'new3', 'New 3', 'detail'])
            self.tv.data.insert(5, [5, 'new5', 'New 5', 'detail'])
            self.tv.insert_rows([3, 5])
            self.tv.end_updates()
            
        
table = TableView2()
