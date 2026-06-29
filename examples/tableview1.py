import json

import ux

with open('uxdocs.json') as in_file:
    uxdocs = json.load(in_file)

class TableView1():
    
    def __init__(self):
        self.tv = ux.TableView()
        self.tv.frame = (0, 0, 580, 620)
        self.tv.flex = 'WH'
        self.tv.name = 'Tableview 1'
        self.tv.delete_enabled = True
        self.tv.move_enabled = True
        self.tv.data_source = self.tv.delegate = self
        self.tv.action = self.table_did_select
        self.tv.accessory_action = self.table_accessory_action
        self.tv.refresh_action = self.refresh
        self.tv.search_action = self.search_handler
        self.btnimage = ux.Image.named('system:moon.stars')  # sfsymbol
        self.edit_button = ux.ButtonItem(title='Edit', action=self.toggle_edit)
        self.tv.right_button_items = [self.edit_button]
        self.tv.menu_items = ['Edit', 'Refresh'] # long press context menu
        self.tv.menu_choice = self.menu_choice

        self.tv.present('sheet')
        self.refresh()

    def search_handler(self, text):
        print('searching... ', text)
        searchstr = str(text).lower()
        dsitems = []
        for item in self.dsitems:
            if searchstr in item['title'].lower():
                dsitems.append(item)
                
        self.tv.data = dsitems
        self.tv.reload()

    def refresh(self, sender=None):
        print('refresh...')
        self.dsitems = []
        classes = uxdocs['classes']
        for i, key in enumerate(classes.keys()):
            self.dsitems.append({'title':classes[key]['name'],
                            'subtitle': classes[key]['constructor'],
                            'style': 'subtitle',
                            'image': self.btnimage,
                            'accessory_type': 'detail_button'
            }) 
        self.tv.end_refresh() # end pull-down refresh
        self.tv.data = self.dsitems
        self.tv.reload()
        
    def menu_choice(self, title, row):
        if title:
            print('title', title, row)
            if title == 'Edit':
                print(self.dsitems[row]['title'])
            elif title == 'Refresh':
                self.refresh()

    def toggle_edit(self, sender):
        print('toggle')
        self.tv.editing = not self.tv.editing
        if self.tv.editing:
            self.edit_button.title = 'Done'
        else:
            self.edit_button.title = 'Edit'
    
    def table_did_select(self, sender):
        print('row %d selected' % self.tv.selected_rows[0][1])

    def table_accessory_action(self, sender):
        print('accessory row %d selected' % self.tv.selected_rows[0][1])

table = TableView1()
