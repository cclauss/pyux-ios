import math
from datetime import date, datetime, time

from rubicon.objc import CGSize, ns_from_py

import ux

from .core import dprint, waitModal, will_block
from .uikit import (
    NSFontAttributeName,
    UIColor,
    UITableViewCell,
    UITableViewCellStyleValue1,
)

asyncq = ux.asyncq

class dialogs():
    def __init__(self):
        pass

    def pick_document(types=['public.item'], return_native=False, callback=None):
        if will_block(callback):
            return None

        pickwait = waitModal()
        filedlg = ux.FilePicker(types=types, result=pickwait.set_result, return_native=return_native, callback=callback)
        filedlg.present()
        if not callback:
            pickwait.wait()
            return pickwait.result

        return None

    def share_text(text):
        share = ux.ShareSheet(type='text', data=text)
        share.present()

    def share_url(url):
        share = ux.ShareSheet(type='url', data=url)
        share.present()

    def share_image(image):
        share = ux.ShareSheet(type='image', data=image)
        share.present()

    def share_items(items):
        share = ux.ShareSheet(type='items', data=items)
        share.present()

    def text_dialog(title='', text='', lines=1, action=None, callback=None):
        if will_block(callback):
            return None

        def close_view(sender):
            container.navigation_view.close(None)

        def done_selected(sender):
            textwait.set_result(str(txt.text), done=False)
            asyncq(close_view)

        def close_selected(sender):
            textwait.set_result(None, done=False)
            asyncq(close_view)
            if callback:
                callback(None)

        def did_close():
            textwait.set_done()
            if callback:
                callback(textwait.result)

        container = ux.View()
        txt = ux.TextView()
        txt.text = text
        txt.font = ('<system>', 18)
        txt.frame = (0, 0, 375, 580)
        imgx = ux.Image.named('system:xmark')
        btnx = ux.ButtonItem(image=imgx, action=close_selected)
        btndone = ux.ButtonItem(title='Done', action=done_selected)
        container.name = title
        container.left_button_items = [btnx]
        container.right_button_items = [btndone]
        container.did_close = did_close
        txt.flex = 'WH'
        container.frame = (0, 0, 375, 580)
        container.flex = 'WH'
        container.add_subview(txt)

        def present(_self):
            container.present(style='sheet', hide_close_button=True)
        asyncq(present)
        textwait = waitModal()
        if not callback:
            textwait.wait()
            return textwait.result

        return None

    def datetime_dialog(title='', mode=2, style=3, callback=None):
        if will_block(callback):
            return None

        def close_view(sender):
            dtview.navigation_view.close(None)

        def done_selected(sender):
            ztime = datetime.strptime(str(dtview.date), '%Y-%m-%d %H:%M:%S %z')
            dprint('ztime', ztime)
            dtmlocal = ztime.astimezone().replace(tzinfo=None)
            if mode == 0:
                dateobj = dtmlocal.time()
            elif mode == 1:
                dateobj = dtmlocal.date()
            elif mode == 2:
                dateobj = dtmlocal
            dtwait.set_result(dateobj, done=False)
            asyncq(close_view)

        def close_selected(sender):
            if not callback:
                dtwait.set_result(None, done=False)
            asyncq(close_view)

        def did_close():
            dtwait.set_done()
            if callback:
                callback(dtwait.result)

        dtview = ux.DatePicker(mode=mode, style=style)
        dtview.name = title
        dtview.did_close = did_close
        btnx = ux.ButtonItem(title='Cancel', action=close_selected)
        btndone = ux.ButtonItem(title='Done', action=done_selected)
        dtview.left_button_items = [btnx]
        dtview.right_button_items = [btndone]

        def present(_self):
            dtview.present(style='sheet', hide_close_button=True)

        asyncq(present)
        dtwait = waitModal()
        if not callback:
            dtwait.wait()
            return dtwait.result

        return None

    def date_dialog(title='', mode=1, style=3, callback=None):
        result = dialogs.datetime_dialog(title=title, mode=mode, style=style, callback=callback)
        return result

    def time_dialog(title='', mode=0, style=1, callback=None):
        result = dialogs.datetime_dialog(title=title, mode=mode, style=style, callback=callback)
        return result

    def list_dialog(title='', items=None, multiple=False, fkitem=None, field=None, frame=None, callback=None):
        if will_block(callback):
            return None

        item_type = 'list'

        def close_view(sender, result=None):
            if tb.searchController:
                tb.controller.navigationItem.searchController.setActive = False
                tb.controller.navigationItem.searchController.removeFromParentViewController()
                tb.controller.navigationItem.searchController = None

            listwait.set_result(result, done=False)

            def close_asyncq(_self):
                tb.native.superview().removeFromSuperview()
                tb.close()

            asyncq(close_asyncq)

        def did_close():
            listwait.set_done()
            if callback:
                if fkitem:
                    callback(fkitem)
                else:
                    callback(listwait.result)

        def table_cell_for_row(tbl, section, row):
            item = tb.data[row]
            if isinstance(item, list):
                return {'title': tb.data[row][1], 'subtitle': '', 'style': 'default', 'accessory': tb.data[row][2]}
            elif isinstance(item, dict):
                title = item.get('title', '')
                accessory = item.get('accessory_type', '')
                return {'title': title, 'subtitle': '', 'style': 'default', 'accessory': accessory}
            elif isinstance(item, str):
                return {'title': str(item), 'subtitle': '', 'style': 'default', 'accessory': 'none'}

        def table_did_select(tableview, section, row):
            result = None
            item = tb.data[row]
            result = item if item != '' else None
            if isinstance(item, list):
                if fkitem is not None:
                    fkitem['id'] = item[0]
                    fkitem['value'] = item[1]

                if field is not None:
                    if callback:
                        field.text = item[1]

            close_view(None, result)

        def search_handler(text):
            searchstr = str(text).lower()
            dsitems = []
            if item_type == 'str':

                for item in items:
                    if searchstr in item.lower():
                        dsitems.append(item)
            else:

                for item in items:
                    if searchstr in item[1].lower():
                        dsitems.append(item)

            tb.data = dsitems
            tb.reload()

        tb = ux.TableView()
        tb.name = title
        tb.backgroundcolor = ux.UIColor.grayColor
        tb.data = items
        tb.tableview_cell_for_row = table_cell_for_row
        tb.tableview_did_select = table_did_select
        if items and len(items) > 9:
            if isinstance(items[0], str):
                item_type = 'str'
            tb.search_action = search_handler

        tb.did_close = did_close
        tb.delete_enabled = False
        if frame:
            x, y, w, h = frame
            dprint('frame', frame)
            tb.controller.preferredContentSize = CGSize(w, h)
        else:
            winw, winh = ux.get_window_size()
            if winw < 580 or winh < 640:
                w, h = (winw, winh)
            else:
                w, h = (580, 640)
                dprint('auto', frame)

        tb.controller.preferredContentSize = CGSize(w, h)

        def present(_self):
            tb.controller.setModalPresentationStyle_(2)
            tb.controller.definesPresentationContext = True
            tb.present('sheet', right_close_button=True)

        asyncq(present)
        listwait = waitModal()
        if not callback:
            listwait.wait()
            return listwait.result

        return None

    def form_dialog(title='', fields=[], sections=None, done_button_title='Done', frame=None, listdone=None, callback=None):
        if will_block(callback):
            return None

        form_title = title
        done_title = done_button_title

        if fields:
            sections = [('', fields)]
        else:
            fields = sections[0][1]

        xmark = ux.Image.named('system:xmark')

        class TextFieldDelegate (object):
            def textfield_should_begin_editing(textfield):
                result = did_begin(textfield)
                return result

        def close_asyncq(_self):
            form.close()
            container.close()

        def close_view(result=None):
            asyncq(close_asyncq)
            wait.set_result(result, done=False)

        def did_close():
            wait.set_done()
            if callback and wait.result:
                callback(wait.result)

        def cancel(sender):
            close_view(None)

        def submit(sender):
            parms = {}
            f = 0
            for sec in sections:
                fields = sec[1]
                for i in range(len(fields)):
                    item = fields[i]
                    if item.get('hidden', False):
                        parms[fields[i]['key']] = fields[i].get('value', '')
                        f += 1
                        continue

                    if item['type'] == 'switch':
                        if isinstance(fields[i].get('value', False), bool):
                            parms[fields[i]['key']] = fld[f].value
                        else:
                            parms[fields[i]['key']] = 1 if fld[f].value else 0
                    elif item['type'] == 'list':
                        parms[fields[i]['key']] = fields[i]['id']
                    elif item['type'] == 'date':
                        if isinstance(fields[i]['value'], str):
                            parms[fields[i]['key']] = str(fld[f].text)
                        else:
                            parms[fields[i]['key']] = fld[f].dateobj
                    elif item['type'] == 'datetime':
                        parms[fields[i]['key']] = fld[f].dateobj
                    elif item['type'] == 'time':
                        parms[fields[i]['key']] = fld[f].dateobj
                    elif item['type'] == 'int':
                        parms[fields[i]['key']] = int(str(fld[f].text))
                    elif item['type'] == 'decimal':
                        parms[fields[i]['key']] = float(str(fld[f].text))
                    elif item['type'] == 'textarea':
                        parms[fields[i]['key']] = str(fld[f].text)
                    elif item['type'] == 'check':
                        if fldvalues[f] > 0:
                            parms[fields[i]['key']] = True
                        else:
                            parms[fields[i]['key']] = False
                    else:
                        parms[fields[i]['key']] = str(fld[f].text)

                    f += 1

            close_view(parms)

        def did_begin(sender):
            offset = 0
            for idx in range(len(secrowsall)):
                if sender.tag > secrowsall[idx] - 1 + offset:
                    offset += secrowsall[idx]
                    continue
                fields = sections[idx][1]
                break

            item = fields[sender.tag - offset]

            if item['type'] == 'list':
                list = item.get('items', None).copy()
                if not list:
                    return False

                for i in range(len(list)):
                    if isinstance(list[i], str):
                        liststr = list[i]
                        list[i] = [liststr, liststr]
                    if len(list[i]) == 2:
                        list[i].append('none')
                    if str(list[i][0]) == str(item.get('id', '')):
                        list[i][2] = 'checkmark'
                    else:
                        list[i][2] = 'none'

                ititle = item['title']
                dialogs.list_dialog(title=ititle, items=list, fkitem=item, field=sender, frame=None, callback=list_end)
                return False

            elif item['type'] in ('time', 'date', 'datetime', 'duration'):
                framew = form.width
                frameh = form.height
                if item['type'] in ('time', 'duration'):
                    style = 1
                else:
                    style = 3

                datepick = ux.DatePicker(mode=item['type'], style=style)
                datepick.native.backgroundColor = UIColor.systemBackgroundColor()
                datepick.action = date_changed
                datepick.tag = sender.tag
                datepick.date = str(sender.text)

                dateview = ux.View()
                dateview.background_color = 'gray'
                dprint(datepick.height) # 216
                dprint(datepick.width)  # 320
                datew = datepick.width
                dateh = datepick.height
                datex = (framew - datew) / 2
                datey = (frameh - dateh) / 2

                dateview.frame = (datex - 5, datey + 15, datew, dateh + 50)
                dateview.add_subview(datepick)

                datebtn = ux.Button()
                datebtn.title = 'Done'
                datebtn.frame = (datew - 70, dateh + 10, 60, 30)
                datebtn.action = datedone
                dateview.add_subview(datebtn)

                datecontainer = ux.View()
                datecontainer.add_subview(dateview)
                form.controller.definesPresentationContext = True
                datecontainer.present('popover', hide_title_bar=True)
                return False
            else:
                return True

        def fromutc(dt):
            dt_offset = dt.utcoffset()
            dt_dst = dt.dst()
            delta = dt_offset - dt_dst

            if delta:
                dt += delta
                dtdst = dt.dst()

            if dtdst:
                return dt + dtdst
            else:
                return dt

        def date_changed(datepicker):
            dprint(datepicker.native.date)
            ztime = datetime.strptime(str(datepicker.native.date), '%Y-%m-%d %H:%M:%S %z')
            dprint('ztime', ztime)
            dtmlocal = ztime.astimezone()
            fld[datepicker.tag].dateobj = dtmlocal.replace(tzinfo=None)
            datestr = datetime.strftime(dtmlocal, fld[datepicker.tag].format)
            fld[datepicker.tag].text = datestr

        def datedone(sender):
            def close_date(_self):
                dprint('close date')
                dateview = sender.superview.superview
                dateview.close()
                return
                dprint('date done', dateview)
                form.remove_subview(dateview)

            asyncq(close_date)

        def did_edit(sender):
            dprint('end')

        def list_end(result):
            if listdone:
                listdone(result, list_value)

        def list_value(fldnum, value):
            fld[fldnum].text = value

        def layout():
            x, y, w, h = form.frame

        def cell_font():
            cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleValue1, "rowtemp")
            cell.textLabel.text = 'title'
            return cell.textLabel.font

        def measure_string(label, font):
            textAttributes = {}
            textAttributes[str(NSFontAttributeName)] = font
            labelFont = ns_from_py(textAttributes)
            size = ns_from_py(label).sizeWithAttributes(labelFont)
            return(math.ceil(size.width), math.ceil(size.height))

        def tableview_cell_for_row(tableview, section, row):
            if form.data[section][row][2] == 'check':
                if fldvalues[form.data[section][row][0]] > 0:
                    return {'title': form.data[section][row][1], 'subtitle':'', 'style': 'default', 'accessory': 'checkmark'}
                else:
                    return {'title': form.data[section][row][1], 'subtitle':'', 'style': 'default', 'accessory': 'none'}

            return {'title': form.data[section][row][1], 'content': form.data[section][row][2],
                'style': 'value1', 'accessory': 'none'}

        def tableview_did_select(tableview, section, row):
            form.content_insets = (0.0, 0.0, 336.0, 0.0)
            if form.data[section][row][2] == 'check':
                if form.get_cell(section, row) > 0:
                    fldvalues[form.data[section][row][0]] = 1
                else:
                    fldvalues[form.data[section][row][0]] = 0

        def tableview_number_of_sections(tableview):
            return len(sections)

        def tableview_title_for_header(tableview, section):
            return sections[section][0]

        def tableview_number_of_rows(tableview, section):
            return secrows[section]

        def tableview_height_for_row(tableview, section, row):
            if isinstance(form.data[section][row][2], ux.TextView):
                return 300
            else:
                return -1

        def kb_frame_will_change(kbframe):
            kbx, kby, kbw, kbh = kbframe
            r = ux.convert_rect(kbframe, to_view=container)

            if kbh > 0:
                if r[3] > 0:
                    kbh = form.height - r[1]
            else:
                kbh = 0
            update_kb_height(kbh)

        def update_kb_height(h):
            if h < 0:
                h = 0
            form.content_inset = (0, 0, h, 0)

        container = ux.View()
        container.did_close = did_close
        form = ux.TableView()
        form.title = title
        form.background_color = 'black'
        form.tableview_cell_for_row = tableview_cell_for_row
        form.tableview_did_select = tableview_did_select
        form.tableview_number_of_sections = tableview_number_of_sections
        form.tableview_title_for_header = tableview_title_for_header
        form.tableview_number_of_rows = tableview_number_of_rows
        form.tableview_height_for_row = tableview_height_for_row
        form.delete_enabled = False
        container.keyboard_will_change = kb_frame_will_change
        form.layout = layout
        tbldata = []
        if frame:
            x, y, w, h = frame
        else:
            winw, winh = ux.get_window_size()
            if winw < 580:
                w, h = (winw, winh)
            elif winh < 640:
                w, h = (winw, winh)
            else:
                w, h = (580, 640)

        i = 0
        fld = []
        fldvalues = []
        secrows = []
        secrowsall = []
        dprint('len', len(sections))
        cellfont = cell_font()
        for section in sections:
            secdata = []
            seccount = 0
            for item in section[1]:
                fld.append(0)
                fldvalues.append(0)
                seccount += 1
                if not item.get('type', None):
                    item['type'] = 'text'
                if not item.get('key', None):
                    item['key'] = i
                if not item.get('title', None):
                    item['title'] = str(item['key'])

                if item.get('hidden', False):
                    i += 1
                    continue

                if item['type'] in ('textarea', 'textview'):
                    fld[i] = ux.TextView()
                    fld[i].text = str(item.get('value', ''))
                    fld[i].tag = i
                    fld[i].font = ('Menlo', 14)
                    fld[i].frame = (125, 15, 250, 280)
                elif item['type']  == 'switch':
                    fld[i] = ux.Switch()
                    if item.get('value', False):
                        fld[i].value = True
                    fld[i].tag = i
                    fld[i].frame = (125, 15, 100, 30)
                elif item['type']  in ('date', 'datetime', 'time'):
                    fld[i] = ux.TextField()

                    date_format = item.get('format', None)
                    if not date_format:
                        if item['type'] == 'date':
                            date_format = '%Y-%m-%d'
                        elif item['type'] == 'time':
                            date_format = '%H:%M'
                        else:
                            date_format = '%Y-%m-%d %H:%M'
                    fld[i].format = date_format

                    value = item.get('value', datetime.now())

                    if type(value) is str:
                        fld[i].text = item['value'][:10]
                    else:
                        if type(value) is date:
                            value = datetime.combine(value, datetime.today().time())
                        if type(value) is time:
                            value = datetime.combine(date.today(), value)
                        fld[i].dateobj = value
                        fld[i].text = value.strftime(fld[i].format)

                    fld[i].tag = i
                    fld[i].textfield_should_begin_editing = did_begin
                elif item['type'] == 'list':
                    fld[i] = ux.TextField()
                    fld[i].text = str(item.get('value', ''))
                    if item.get('id', None) is None:
                        item['id'] = item.get('value', '')
                    fld[i].tag = i
                    fld[i].textfield_should_begin_editing = did_begin
                elif item['type'] == 'decimal':
                    fld[i] = ux.TextField()
                    fld[i].text = '{:{align}.{prec}f}'.format(round(float(item.get('value', 0.00)), 2), align='<', prec=2)
                    fld[i].tag = i
                    fld[i].keyboard_type = ux.KEYBOARD_DECIMAL_PAD
                elif item['type'] == 'check':
                    fld[i] = 'check'
                    if item.get('value', None):
                        fldvalues[i] = 3
                elif item['type'] in ('int', 'text', 'url', 'email', 'number', 'password'):
                    fld[i] = ux.TextField()
                    fld[i].text = str(item.get('value', ''))
                    fld[i].tag = i
                else:
                    print('%s is an invalid type parameter' % str(item['type']))
                    break

                if item['type'] not in ('check', 'textarea', 'textview'):
                    label_width, label_height = measure_string(item['title'], cellfont) #[0] + 16
                    dprint(item['title'], label_width, label_height)
                    if label_width > 180:
                        fld[i].frame = (label_width + 30, 6, w - label_width - 50, label_height + 14)
                    elif label_width > 160:
                        fld[i].frame = (190, 6, w - 210 , label_height + 14)
                    elif label_width > 130:
                        fld[i].frame = (160, 6, w - 180 , label_height + 14)
                    elif label_width > 100:
                        fld[i].frame = (130, 6, w - 150 , label_height + 14)
                    else:
                        fld[i].frame = (120, 6, w - 140 , label_height + 14)
                    fld[i].flex = 'R'

                if item['type'] in ('text', 'textarea', 'textview'):
                    fld[i].autocorrection_type = item.get('autocorrection', None)
                    fld[i].autocapitalization_type = item.get('autocapitalization', ux.AUTOCAPITALIZE_SENTENCES)
                    fld[i].spellchecking_type = item.get('spellchecking', None)
                elif item['type'] == 'url':
                    fld[i].keyboard_type = ux.KEYBOARD_URL
                    fld[i].autocapitalization_type = ux.AUTOCAPITALIZE_NONE
                    fld[i].autocorrection_type = False
                    fld[i].spellchecking_type = False
                elif item['type'] == 'email':
                    fld[i].keyboard_type = ux.KEYBOARD_EMAIL
                    fld[i].autocapitalization_type = ux.AUTOCAPITALIZE_NONE
                    fld[i].autocorrection_type = False
                    fld[i].spellchecking_type = False
                elif item['type'] == 'number':
                    #fld[i].keyboard_type = ux.KEYBOARD_NUMBERS
                    fld[i].keyboard_type = ux.KEYBOARD_NUMBER_PAD
                    fld[i].autocapitalization_type = ux.AUTOCAPITALIZE_NONE
                    fld[i].autocorrection_type = False
                    fld[i].spellchecking_type = False
                elif item['type'] == 'password':
                    fld[i].secure = True

                secdata.append([i, item['title'], fld[i]])
                i += 1
            tbldata.append(secdata)
            dprint(seccount)
            secrows.append(len(secdata))
            secrowsall.append(seccount)

        dprint('secrows', secrows)
        form.data = tbldata

        def present(_self):
            container.name = form_title
            container.left_button_items = [ux.ButtonItem(image=xmark, action=cancel)]
            container.right_button_items = [ux.ButtonItem(title=done_title, action=submit)]
            form.frame = (0, 0, w, h)
            form.flex = 'WH'
            container.frame = (0, 0, w, h)
            container.flex = 'WH'
            container.add_subview(form)
            form.controller.preferredContentSize = CGSize(w, h)
            container.present('sheet', hide_title_bar=False, hide_close_button=True)

        asyncq(present)

        wait = waitModal()
        if not callback:
            wait.wait()
            if wait.result == 'cancel':
                return None
            return wait.result

        return None
