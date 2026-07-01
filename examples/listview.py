import json

import ux as ui

"""
The built-in PyUx TableView datasource contains much of the same functionality as ListDataSource.
A Pythonista style ListDataSource is included to aid with Pythonista script migrations.
"""

with open('uxdocs.json') as in_file:
    uxdocs = json.load(in_file)

class TableView1():

    def __init__(self):
        self.tv = ui.TableView()
        self.tv.frame = (0, 0, 580, 620)
        self.tv.flex = 'WH'
        self.tv.name = 'List Datasource'
        self.tv.background_color = 'gray'
        self.ds = ui.ListDataSource([])
        self.tv.data_source = self.tv.delegate = self.ds
        self.ds.text_color = None
        self.ds.highlight_color = None
        self.ds.number_of_lines = 1
        self.ds.delete_enabled = True
        self.ds.move_enabled = True
        self.ds.action = self.tableview_did_select
        self.ds.accessory_action = self.tableview_accessory_action
        self.btnimage = ui.Image.named('system:ellipsis.circle')
        self.edit_button = ui.ButtonItem(title='Edit', action=self.toggle_edit)
        self.tv.right_button_items = [self.edit_button]
        self.tv.present('sheet')
        self.refresh()

    def refresh(self):
        dsitems = []
        classes = uxdocs['classes']
        for i, key in enumerate(classes.keys()):
            dsitems.append({'title':classes[key]['name'],
                            'subtitle': classes[key]['constructor'],
                            'style': 'subtitle',
                            'image': self.btnimage,
                            'accessory_type': 'detail_button'
            })
        self.ds.items = dsitems

    def toggle_edit(self, sender):
        print('toggle', sender)
        self.tv.editing = not self.tv.editing
        if self.tv.editing:
            self.edit_button.title = 'Done'
        else:
            self.edit_button.title = 'Edit'

    def tableview_cell_for_row(self, tableview, section, row):
        return {'title': self.tv.data[row][2],
                'subtitle': '  ' + self.tv.data[row][3],
                'style': 'subtitle',
                'accessory': 'detail_button'
        }

    def tableview_did_select(self, sender):
        print('row %d selected' % self.tv.selected_rows[0][1])

    def tableview_accessory_action(self, sender):
        print('accessory row %d selected' % self.tv.selected_rows[0][1])


TableView1()
