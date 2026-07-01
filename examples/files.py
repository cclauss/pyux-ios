import os
import runpy
import shutil
import sys
import time

import ux
import ux.alerts as console
from ux.dialogs import dialogs


class FileOps (object):
    def __init__(self):
        self.filelist = []
        self.typelist = []
        self.CutCopy = None
        self.cutview = None

    def set_filelist(self, list):
        self.filelist = list

    def reload_data(self, tv):
        tv.reload_data()

    def newfile(self, newtype, dirpath, newname):
        newfile = os.path.join(dirpath, newname)
        try:
            if newtype == 'folder':
                try:
                    os.mkdir(newfile)
                except IOError:
                    return 'error'
            else:
                if os.path.isfile(newfile):
                    return 'error'
                try:
                    f = open(newfile, 'w')
                    f.close()
                except IOError:
                    return 'error'
        except Exception:
            return 'error'
        return 'ok'

    def cut(self, tv):
        self.CutCopy = 'cut'
        self.cutview = tv

    def copy(self):
        self.CutCopy = 'copy'

    def paste(self, path):
        if self.CutCopy == 'cut':
            result = self.pastecut(path)
        else:
            result = self.pastecopy(path)
        return result

    def pastecut(self, path):
        self.CutCopy = None
        r = 0
        for row in self.filelist:
            try:
                if row[2]==0:
                    shutil.move(row[0] + os.sep + row[1], path + os.sep + row[1])
                else:
                    shutil.move(row[0] + os.sep + row[1], path)
            except Exception:
                print("Exception: ",str(sys.exc_info()))
                console.hud_alert(str(sys.exc_info()))
                return 'error'
            r += 1
        return 'ok'

    def pastecopy(self, path):
        self.CutCopy = None
        r = 0
        for row in self.filelist:
            destpath = path + os.sep + row[1]
            try:
                if row[2]==0:
                    shutil.copytree(row[0] + os.sep + row[1], destpath)
                else:
                    shutil.copy2(row[0] + os.sep + row[1], destpath)
            except Exception:
                console.hud_alert(str(sys.exc_info()))
                print(path)
                print(self.filelist)
                print ("Exception copy",str(sys.exc_info()))
                return 'error'
            r += 1
        return 'ok'

    def delete(self):
        for row in self.filelist:
            try:
                if row[2]==0:
                    # delete folder
                    path = row[0] + os.sep + row[1] + os.sep
                    if os.name == 'nt':
                        os.system('rmdir /S /Q \"{}\"'.format(path))
                    else:
                        path = row[0] + os.sep + row[1]
                        shutil.rmtree(path)
                else:
                    # delete file
                    os.remove(row[0] + os.sep + row[1])
            except Exception:
                print("Exception ",str(sys.exc_info()))
                return 'error'

        self.filelist = []
        return 'ok'

class FilesView():
    def __init__(self, name, path, rootpath, fileops, level):
        self.name = name
        self.path = path
        self.rootpath = rootpath
        self.fileops = fileops
        self.level = level
        self.tv = ux.TableView()
        self.tv.name = os.path.basename(self.path)
        self.tv.data_source = self.tv.delegate = self
        self.tv.action = self.table_did_select
        self.tv.accessory_action = self.table_accessory_action
        #self.tv.tableview_cell_for_row = self.tableview_cell_for_row
        #self.tv.tableview_delete = self.tableview_delete
        self.tv.data = []
        # long press context menu
        self.tv.menu_items = ['Cut', 'Copy', 'Paste', 'Delete', 'Rename', 'New', 'Refresh']
        self.tv.menu_choice = self.menu_choice
        menuitems = [('New', self.btn_action), ('Import', self.btn_action), ('Refresh', self.btn_action)]
        menu = ux.Menu('Actions', menuitems)
        self.tv.right_button_items = [ux.ButtonItem(title='Menu', action=None, menu=menu)]
        self.dataset = 'files'
        self.refresh(self.path)

    def refresh(self, path):
        self.reload(path)

    def reload(self, path):
        # Refresh the list of files and folders
        self.tv.data = []
        try:
            _, folders, files = next(os.walk(path))
        except Exception:
            print('access denied')
            console.hud_alert('access denied')
            return

        if path != self.rootpath:
            self.tv.data.append({'title': '..', 'type': 'folder', 'path': '..', 'accessory_type': 'none'})
        folders = sorted(folders, key=lambda s: s.lower())
        files = sorted(files, key=lambda s: s.lower())
        for item in folders:
            self.tv.data.append({'title': item, 'type': 'folder', 'path': path, 'accessory_type': 'none'})
        for item in files:
            self.tv.data.append({'title': item, 'type': 'file', 'path': path, 'accessory_type': 'none'})

        self.path = path
        self.tv.name = os.path.basename(self.path)
        print('reload')
        self.tv.reload()

    def tableview_cell_for_row(self, tableview, section, row):

        item = self.tv.data[row]
        ftype = item['type']
        if ftype == 'folder':
            if item['title'] == '..':
                return {'title': item['title'], 'subtitle': ftype, 'style': 'subtitle',
                    'accessory_type': 'none', 'image':folderimg}
            else:
                return {'title': item['title'], 'subtitle': ftype, 'style': 'subtitle',
                    'accessory_type': 'disclosure_indicator', 'image':folderimg}
        else:
            filename = item['title']
            fullname = os.path.join(self.path, filename)
            stats =  os.stat(fullname)
            filedtm = time.strftime('%Y-%m-%d %H:%M',time.localtime(stats.st_mtime))
            return {'title': item['title'], 'subtitle': filedtm, 'style': 'subtitle',
                'accessory_type': 'detail_button', 'image':fileimg}

    def table_did_select(self, sender):
        print('row %s selected' % str(self.tv.selected_row))
        section, row = self.tv.selected_row
        ftype = self.tv.data[row]['type']
        if ftype == 'folder':
            dirname = self.tv.data[row]['title']
            if dirname == '..':
                self.tv.navigation_view.pop_view()
            else:
                newpath = os.path.join(self.path, dirname)
                #print(newpath)
                if len(navviews) > self.level and sys.platform == 'ios':
                    print('old class')
                    next = navviews[self.level]
                    next.refresh(newpath)
                else:
                    print('new class')
                    next = FilesView(dirname, newpath, self.rootpath, fileops, self.level + 1)
                    navviews.append(next)
                self.tv.navigation_view.push_view(next.tv)

        else:
            script = os.path.join(self.path, self.tv.data[row]['title'])
            for n in reversed(range(len(ux.uxviews))):
                if ux.uxviews[n] == 'newapp':
                    ux.uxviews.pop(n)
            ux.uxviews.insert(0, 'newapp')

            ext = os.path.splitext(script)[1]
            if ext == '.py':
                self.run_py3(script)

    def table_accessory_action(self, sender):
        row = self.tv.selected_rows[0][1]
        self.action_menu(sender, 0, row)

    def tableview_delete(self, tableview, section, row):
        print('delete: ', row)
        self.actions([row, 'Delete'])

    def run_py3(self, script):

        def _run_async(_self):
            runpy.run_path(script, run_name='__main__')

        ux.asyncq(_run_async)

    def action_menu(self, tableview, section, row):

        list = [[row, 'Cut', 'none'], [row, "Copy", 'none'], [row, "Paste", 'none'],
            [row, "Rename", 'none'], [row, "New", 'none'], [0, "Refresh", 'none']]

        dialogs.list_dialog(title='Acions', items=list, fkitem=None, field=tableview, frame=None, callback=self.actions)

    def btn_action(self, sender, args=None):
        action = sender.Header if sys.platform == 'win32' else sender.title
        print('action', action)
        self.actions([0, action])

    def menu_choice(self, title, row=0):
        print(title,'-', row)
        self.actions([row, title])

    def actions(self, result):
        if not result:
            return
        row = result[0]
        action = result[1]
        if action == 'Refresh':
            self.refresh(self.path)

        elif action == 'New':
            fields = [{'key': 'name', 'title': 'New dir', 'type': 'text', 'value':'newdir'}]
            newname = dialogs.form_dialog(title='New dir', fields=fields, callback=self.do_new)
            if newname is not None:
                result = fileops.newfile('folder', self.path, newname['name'])
                if result == 'ok':
                    self.refresh(self.path)
                else:
                    console.hud_alert(result)

        elif action == 'Rename':
            self.filelist(self.tv)
            if len(fileops.filelist) == 0:
                return
            namepart = fileops.filelist[0][1]
            fileops.filelist = []
            fields = [{'key': 'name', 'title': 'Rename', 'type': 'text', 'value':namepart},
                        {'key': 'namepart', 'title': '', 'type': 'text', 'hidden': True, 'value':namepart}]
            dialogs.form_dialog(title='New name', fields=fields, callback=self.do_rename)

        elif action == 'Import':

            def _callback(files):
                if files:
                    for file in files:
                        print(file)
                        shutil.copy2(file, self.path)
                    self.refresh(self.path)

            dialogs.pick_document(types=['public.item'], callback=_callback)

        elif action == 'Cut':
            self.filelist(self.tv)
            result = fileops.cut(self)

        elif action == 'Copy':
            self.filelist(self.tv)
            result = fileops.copy()

        elif action == 'Paste':
            if len(fileops.filelist) == 0:
                return
            result = fileops.paste(self.path)
            if result == 'ok':
                if fileops.cutview is not None:
                    fileops.cutview.refresh(fileops.cutview.path)
                self.refresh(self.path)

        elif action == 'Delete':
            self.filelist1(row)
            confirm = ''
            for row in fileops.filelist:
                confirm += row[1] + '\n'

            def _callback(response):
                if response:
                    result = fileops.delete()
                    if result == 'ok':
                        self.refresh(self.path)

            ux.confirm_dialog('Delete', confirm, _callback)

    def do_rename(self, response):
        print('rename', response)
        if response is not None:
            fullfile = self.path + os.sep + response['namepart']
            fullnew = self.path + os.sep + response['name']
            try:
                os.rename(fullfile,fullnew)
            except Exception:
                console.hud_alert('error')
            self.refresh(self.path)

    def do_new(self, response):
        print('new dir', response)
        if response is not None:
            result = fileops.newfile('folder', self.path, response['name'])
            if result == 'ok':
                self.refresh(self.path)
            else:
                console.hud_alert(result)

    def filelist1(self, row):
        filelist = []
        name = self.tv.data[row]['title']
        if name == '..':
            return
        if self.tv.data[row]['type'] == 'folder':
            filelist.append([self.path, name, 0])
        else:
            filelist.append([self.path, name, 1])
        fileops.set_filelist(filelist)

    def filelist(self, tv):
        filelist = []
        for item in tv.selected_rows:
            row = item[1]
            name = self.tv.data[row]['title']
            if name == '..':
                continue
            if self.tv.data[row]['type'] == 'folder':
                filelist.append([self.path, name, 0])
            else:
                filelist.append([self.path, name, 1])

        fileops.set_filelist(filelist)


navviews = []
if ux.py3kit:
    # pythonista
    rootpath = os.path.expanduser('~')
    localpath = os.path.expanduser('~')
else:
    rootpath = os.path.expanduser('~/Documents')
    localpath = os.path.expanduser('~/Documents')

print(localpath)
fileops = FileOps()

if sys.platform == 'ios':
    if ux.get_window_traits()['style'] == 'dark':
        imgx = ux.Image.named('system:xmark')
        folderimg = ux.Image.named('iow:ios7_folder_outline_32.png')
        fileimg = ux.Image.named('iow:document_32.png')
        menuimg = ux.Image.named('system:xmark')
    else:
        imgx = ux.Image.named('system:xmark')
        folderimg = ux.Image.named('iob:ios7_folder_outline_32.png')
        fileimg = ux.Image.named('iob:document_32.png')
        menuimg = ux.Image.named('system:xmark')
else:
    folderimg = 'folder'
    fileimg = 'file'

class NavView():
    def __init__(self, name, localpath, rootpath):
        local = FilesView('Local', localpath, rootpath, fileops, 0)

        self.view = local.tv
        nav = ux.NavigationView(local.tv)
        if sys.platform == 'win32':
            nav.present()
        else:
            nav.present('sheet', right_close_button=True, topbar=True, title='Files')


class UxApp():

    def __init__(self):
        NavView('Nav', localpath, rootpath)

if __name__ == '__main__':
    UxApp()
