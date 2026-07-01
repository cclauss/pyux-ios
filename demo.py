import os
import runpy
import time

import ux


class Launcher():

    def __init__(self):
        self.tv = ux.TableView()
        self.tv.frame = (0, 0, 580, 620)
        self.tv.flex = 'WH'
        self.tv.name = 'UX Demo'

        self.tv.delete_enabled = False
        self.tv.move_enabled = False
        self.tv.data_source = self.tv.delegate = self
        self.tv.action = self.tableview_select
        self.tv.refresh_action = self.refresh
        self.tv.did_close = self.did_close
        menuimage = ux.Image.named('system:ellipsis.circle')
        menuitems = [
            ('Exit', self.tv.close)
        ]
        btmmenu = ux.Menu('Actions', menuitems)
        self.button = ux.ButtonItem(image=menuimage, action=None, menu=btmmenu)
        self.tv.left_button_items = [self.button]
        self.tv.present('sheet', right_close_button=True)
        self.savepath = os.getcwd()
        self.path = os.path.join(os.getcwd(), 'examples')
        os.chdir(self.path)
        self.refresh()

    def refresh(self, sender=None):
        self.dsitems = []
        try:
            _, folders, files = next(os.walk(self.path))
        except Exception as e:
            print(f'access denied: {e}')
            return

        files = sorted(files, key=lambda s: s.lower())
        for file in files:
            if not os.path.splitext(file)[1] == '.py':
                continue
            title = (os.path.splitext(file)[0]).title()
            fullname = os.path.join(self.path, file)
            stats =  os.stat(fullname)
            filedtm = time.strftime('%Y-%m-%d %H:%M',time.localtime(stats.st_mtime))

            self.dsitems.append({'title': title,
                            'filename': file,
                            'subtitle': filedtm,
                            'style': 'default',
                            'accessory_type': 'detail_button'
            })

        self.tv.data = self.dsitems
        self.tv.end_refresh()
        self.tv.reload()

    def did_close(self):
        os.chdir(self.savepath)

    def run_py3(self, script):
        def _run_async(_self):
            runpy.run_path(script, run_name='__main__')

        os.chdir(self.path)
        ux.asyncq(_run_async)

    def tableview_select(self, sender):
        print('row %d selected' % self.tv.selected_rows[0][1])
        filename = self.tv.data[self.tv.selected_rows[0][1]]['filename']
        self.run_py3(os.path.join(self.path, filename))


Launcher()
