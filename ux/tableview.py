from rubicon.objc import Block, NSPoint, ObjCClass, ObjCInstance, ObjCProtocol, SEL, ns_from_py, objc_method, objc_property, send_message, send_super
from rubicon.objc.runtime import get_class, objc_id
from ctypes import c_int
from .core import asyncq, dprint
from .colors import uicolor, uicolor_rgba
from .font import Font
from .menu import Action
from .tableviewcell import TableViewCell
from .view import View
from .viewcore import ViewCore

from .foundation import NSIndexPath

from .uikit import (
    UIAction,
    UIColor,
    UIFont,
    UIControlEventValueChanged,
    UIMenu,
    UIRefreshControl,
    UITableViewCell,
    UITableViewCellEditingStyleDelete,
    UITableViewCellEditingStyleInsert,
    UITableViewCellEditingStyleNone,
    UITableViewCellStyleDefault,
    UITableViewCellStyleSubtitle,
    UITableViewCellStyleValue1,
    UITableViewCellStyleValue2,
    UITableViewController,
    UITableViewScrollPositionNone
)

UISearchController = ObjCClass('UISearchController')
UIBackgroundConfiguration = ObjCClass('UIBackgroundConfiguration')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')
UIContextMenuConfiguration = ObjCClass('UIContextMenuConfiguration')

UIViewAutoresizingNone = 0
UIViewAutoresizingFlexibleLeftMargin = 1 << 0
UIViewAutoresizingFlexibleWidth = 1 << 1
UIViewAutoresizingFlexibleRightMargin = 1 << 2
UIViewAutoresizingFlexibleTopMargin = 1 << 3
UIViewAutoresizingFlexibleHeight = 1 << 4
UIViewAutoresizingFlexibleBottomMargin = 1 << 5


def get_tableview():
    if get_class('uxTableViewController').value is not None:
        return ObjCClass(get_class('uxTableViewController'))
    else:
        class uxTableViewController(UITableViewController):

            interface = objc_property(object, weak=True)

            @objc_method
            def viewDidLoad(self) -> None:
                dprint('tableView did load')

            @objc_method
            def viewWillAppear_(self) -> None:
                #send_super(__class__, self, "viewWillAppear")
                dprint("tableView will appear")
                self.interface.layout()

            @objc_method
            def viewSafeAreaInsetsDidChange(self) -> None:
                send_super(__class__, self, "viewSafeAreaInsetsDidChange")
                dprint("tableView insets changed")
                self.interface._insets_changed()

            @objc_method
            def viewWillLayoutSubviews(self) -> None:
                send_super(__class__, self, "viewWillLayoutSubviews")
                dprint("tableView will layout")
                self.interface.will_layout()

            @objc_method
            def viewDidLayoutSubviews(self) -> None:
                send_super(__class__, self, "viewDidLayoutSubviews")
                dprint("tableView did layout")
                self.interface.did_layout()

            @objc_method
            def viewDidAppear_(self, animated: bool) -> None:
                self.interface.ispresented = True
                dprint("tableView appeared")
                self.interface.did_appear()

            @objc_method
            def viewWillDisappear_(self) -> None:
                dprint("tableView will disappear")
                self.interface.will_close()

            @objc_method
            def viewDidDisappear_(self, animated: bool) -> None:
                self.interface.ispresented = False
                dprint("tableView disappeared", animated)
                self.interface._did_close()

            @objc_method
            def numberOfSectionsInTableView_(self) -> int:
                dprint('number--sections')
                return 	self.interface.tableview_number_of_sections(self)

            @objc_method
            def tableView_titleForHeaderInSection_(self, tableView, section: int):
                return self.interface.tableview_title_for_header(tableView, section)

            @objc_method
            def tableView_numberOfRowsInSection_(self, tableView, section: int) -> int:
                return 	self.interface.tableview_number_of_rows(tableView, section)

            @objc_method
            def tableView_cellForRowAtIndexPath_(self, tableView, indexPath):
                cell = self.interface.tableview_cell_for_row_at_indexpath(tableView, indexPath)
                cell.retain()
                return cell

            @objc_method
            def tableView_canMoveRowAtIndexPath_(self, tableView, indexPath) -> bool:
                return self.interface.tableview_can_move(tableView, indexPath.section, indexPath.row)

            @objc_method
            def tableView_moveRowAtIndexPath_toIndexPath_(self, tableView, atIndexPath, toIndexPath):
                self.interface.tableview_move_row(tableView, atIndexPath.section, atIndexPath.row, toIndexPath.section, toIndexPath.row)

            @objc_method
            def tableView_editingStyleForRowAtIndexPath_(self, tableView, indexPath) -> int:
                return self.interface.tableview_editing_style(tableView, indexPath.section, indexPath.row)

            @objc_method
            def tableView_canEditRowAtIndexPath_(self, tableView, indexPath) -> bool:
                return self.interface.tableview_can_edit(tableView, indexPath.section, indexPath.row)

            @objc_method
            def tableView_shouldIndentWhileEditingRowAtIndexPath_(self, tableView, indexPath) -> bool:
                return self.interface.tableview_can_delete(tableView, indexPath.section, indexPath.row)

            @objc_method
            def tableView_commitEditingStyle_forRowAtIndexPath_(self, tableView, editingStyle: int, indexPath):
                if editingStyle == UITableViewCellEditingStyleDelete:
                    if editingStyle == UITableViewCellEditingStyleDelete:
                        tableView.selectRowAtIndexPath_animated_scrollPosition_(indexPath, False, 0)
                        if self.interface.tableview_delete:
                            self.interface.tableview_delete(tableView, indexPath.section, indexPath.row)
                    elif editingStyle == UITableViewCellEditingStyleInsert:
                        pass
                    elif editingStyle == UITableViewCellEditingStyleNone:
                        pass

            @objc_method
            def onRefresh_(self, obj) -> None:
                if self.interface.refresh_handler:
                    self.interface.refresh_handler(self.interface)

            @objc_method
            def updateSearchResultsForSearchController_(self, searchController):
                text = searchController.searchBar.text
                if self.interface.search_handler:
                    self.interface.search_handler(text)

            @objc_method
            def tableView_contextMenuConfigurationForRowAtIndexPath_point_(self, tableView, indexPath, point: NSPoint):
                tableView.selectRowAtIndexPath_animated_scrollPosition_(indexPath, False, 0)
                config = self.interface.tableview_context_menu(tableView, indexPath.row)
                return config

            @objc_method
            def tableView_didSelectRowAtIndexPath_(self, tableView, indexPath):
                self.interface.tableview_did_select(tableView, indexPath.section, indexPath.row)

            @objc_method
            def tableView_didDeselectRowAtIndexPath_(self, tableView, indexPath):
                self.interface.tableview_did_deselect(tableView, indexPath.section, indexPath.row)

            @objc_method
            def tableView_titleForDeleteConfirmationButtonForRowAtIndexPath_(self, tableView, indexPath):
                return self.interface.tableview_title_for_delete_button(tableView, indexPath.section, indexPath.row)

            @objc_method
            def tableView_accessoryButtonTappedForRowWithIndexPath_(self, tableView, indexPath):
                tableView.selectRowAtIndexPath_animated_scrollPosition_(indexPath, False, 0)
                self.interface.tableview_accessory_button_tapped(tableView, indexPath.section, indexPath.row)


            @objc_method
            def tableView_heightForRowAtIndexPath_(self, tableView, indexPath) -> float:
                return self.interface.tableview_height_for_row(tableView, indexPath.section, indexPath.row)

        return uxTableViewController

class TableView(ViewCore):

    def __init__(self, **kwargs):
        self.init()
        self.data = []
        tvclass = get_tableview()
        self.controller = tvclass.alloc().init()
        self.controller.interface = self
        self.native = self.controller.tableView
        self.controller.tableView.interface = self
        self.searchController = None
        self.ispresented = False
        self._data_source = self
        self._delegate = self
        self.name = None
        self.right_items = None
        self.lastrow = -1
        self.menu_items = []
        self.navbar = None
        self.action = None
        self.accessory_action = None
        self.edit_action = None
        self.delete_enabled = True
        self.move_enabled = True

        dprint('tableview')
        for arg in kwargs:
            if self.viewattrs(arg, kwargs[arg]):
                continue
            """
            if arg == 'name':
                self.name = kwargs[arg]
            """

    @property
    def allows_multiple_selection(self):
        return self.native.allowsMultipleSelection

    @allows_multiple_selection.setter
    def allows_multiple_selection(self, value):
        if type(value) is bool:
            self.native.allowsMultipleSelection = value

    @property
    def allows_multiple_selection_during_editing(self):
        return self.native.allowsMultipleSelectionDuringEditing

    @allows_multiple_selection_during_editing.setter
    def allows_multiple_selection_during_editing(self, value):
        if type(value) is bool:
            self.native.allowsMultipleSelectionDuringEditing = value

    @property
    def allows_selection(self):
        return self.native.allowsSelection

    @allows_selection.setter
    def allows_selection(self, value):
        if type(value) is bool:
            self.native.allowsSelection = value

    @property
    def allows_selection_during_editing(self):
        return self.native.allowsSelectionDuringEditing

    @allows_selection_during_editing.setter
    def allows_selection_during_editing(self, value):
        if type(value) is bool:
            self.native.allowsSelectionDuringEditing = value

    def begin_refresh(self):
        self.controller.refreshControl.beginRefreshing()

    def end_refresh(self):
        self.controller.refreshControl.endRefreshing()

    def begin_updates(self):
        self.native.beginUpdates()

    def end_updates(self):
        self.native.endUpdates()

    def refresh_data(self, sender):
        self.controller.refreshControl.endRefreshing()

    @property
    def content_inset(self):
        return self.native.isEditing()

    @content_inset.setter
    def content_inset(self, value):
        t, left, b, r = value
        def _async(_self):
            contentInset = self.native.contentInset
            contentInset.bottom = b
            scrollInsets = self.native.scrollIndicatorInsets
            scrollInsets.bottom = b
            self.native.contentInset = contentInset
            self.native.scrollIndicatorInsets = scrollInsets
        asyncq(_async)

    @property
    def editing(self):
        return self.native.isEditing()

    @editing.setter
    def editing(self, value):
        self.native.setEditing(value)

    def on_presented(self):
        return self.ispresented

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, cls):
        self._data_source = cls
        if hasattr(cls, 'tableview_number_of_sections'):
            self.tableview_number_of_sections = cls.tableview_number_of_sections

        if hasattr(cls, 'tableview_number_of_rows'):
            self.tableview_number_of_rows = cls.tableview_number_of_rows

        if hasattr(cls, 'tableview_cell_for_row'):
            self.tableview_cell_for_row = cls.tableview_cell_for_row

        if hasattr(cls, 'tableview_title_for_header'):
            self.tableview_title_for_header = cls.tableview_title_for_header

        if hasattr(cls, 'tableview_can_delete'):
            self.tableview_can_delete = cls.tableview_can_delete

        if hasattr(cls, 'tableview_can_edit'):
            self.tableview_can_edit = cls.tableview_can_edit

        if hasattr(cls, 'tableview_can_move'):
            self.tableview_can_move = cls.tableview_can_move

        if hasattr(cls, 'tableview_editing_style'):
            self.tableview_editing_style = cls.tableview_editing_style

        if hasattr(cls, 'tableview_delete'):
            self.tableview_delete = cls.tableview_delete

        if hasattr(cls, 'tableview_move_row'):
            self.tableview_move_row = cls.tableview_move_row

        if hasattr(cls, 'tableview_height_for_row'):
            self.tableview_height_for_row = cls.tableview_height_for_row

    @property
    def delegate(self):
        return (self._delegate)

    @delegate.setter
    def delegate(self, cls):
        self._delegate = cls

        if hasattr(cls, 'tableview_did_select'):
            self.tableview_did_select = cls.tableview_did_select

        if hasattr(cls, 'tableview_did_deselect'):
            self.tableview_did_deselect = cls.tableview_did_deselect

        if hasattr(cls, 'tableview_title_for_delete_button'):
            self.tableview_title_for_delete_button = cls.tableview_title_for_delete_button

        if hasattr(cls, 'tableview_accessory_button_tapped'):
            self.tableview_accessory_button_tapped = cls.tableview_accessory_button_tapped

    @property
    def header_view(self):
        return self.native.tableHeaderView.interface

    @header_view.setter
    def header_view(self, view):
        self.native.setTableHeaderView_(view.native)

    def menu_action(self, sender) -> None:
        dprint('-' * 16)
        self.menu_choice(str(ObjCInstance(sender).title), self.lastrow)

    def menu_choice(self, title, row):
        dprint(title,' ', row)
        dprint('-' * 16)

    def new_action(self, actdict):
        return Action(
            actdict.get('title', None),
            self.menu_action,
            actdict.get('image', None),
            actdict.get('attributes', None)
        )

    def create_menu(self, action: objc_id):
        menuactions = []
        for item in self.menu_items:
            if isinstance(item, dict):
                menu_action = self.new_action(item).native
            else:
                if isinstance(item[1], list):
                    menu_action = self.sub_menu(item[0], item[1])
                else:
                    menu_handler_block=Block(self.menu_action, None, objc_id)
                    menu_action = UIAction.actionWithHandler_(menu_handler_block)
                    menu_action.title = item
            if menu_action:
                menuactions.append(menu_action)

        menu_action = UIAction.actionWithHandler_(None)
        menu_action.title = ' '
        menuactions.append(menu_action)

        menu = UIMenu.menuWithTitle(str('Actions'), children=menuactions)
        return menu.ptr.value

    def sub_menu(self, title, items):
        menuactions = []
        for item in items:
            if isinstance(item, dict):
                menu_action = self.new_action(item).native
            else:
                if isinstance(item[1], list):
                    menu_action = self.sub_menu(item[0], item[1])
                else:
                    menu_handler_block=Block(self.menu_action, None, objc_id)
                    menu_action = UIAction.actionWithHandler_(menu_handler_block)
                    menu_action.title = item
            if menu_action:
                menuactions.append(menu_action)
        menu_action = UIAction.actionWithHandler_(None)
        menu_action.title = ' '
        menuactions.append(menu_action)

        submenu = UIMenu.menuWithTitle(str(title), children=menuactions)
        return submenu

    @property
    def row_height(self):
        return self.native.rowHeight

    @row_height.setter
    def row_height(self, height):
        self.native.rowHeight = height

    @property
    def selected_row(self):
        rowset = []
        selected_rows = self.native.indexPathsForSelectedRows
        if selected_rows is None:
            return None
        for item in selected_rows:
            section_row = ObjCInstance(item)
            try:
                sec = section_row.section
                row = section_row.row
            except:
                sec = section_row.section()
                row = section_row.row()
            rowset.append((sec, row))

        return rowset[0]

    @selected_row.setter
    def selected_row(self, index):
        if type(index) is tuple:
            index_path = NSIndexPath.indexPathForRow(index[1], inSection=index[0])
            self.native.selectRowAtIndexPath(index_path,
                animated=True, scrollPosition=0
            )

    @property
    def selected_rows(self):
        rowset = []
        selected_rows = self.native.indexPathsForSelectedRows
        if selected_rows is None:
            return None
        for item in selected_rows:
            section_row = ObjCInstance(item)
            try:
                sec = section_row.section
                row = section_row.row
            except:
                sec = section_row.section()
                row = section_row.row()
            rowset.append((sec, row))

        return rowset

    @selected_rows.setter
    def selected_rows(self, rowset):
        for index in rowset:
            self.selected_row = index

    @property
    def separator_color(self):
        return uicolor_rgba(self.native.separatorColor)

    @separator_color.setter
    def separator_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.native.separatorColor = ncolor

    def tableview_number_of_sections(self, tv):
        dprint('-- number sections --')
        return 1

    def tableview_number_of_rows(self, tableview, section):
        return len(self.data)

    def tableview_cell_for_row_at_indexpath(self, tableView, indexPath):
        value = self.tableview_cell_for_row(tableView, indexPath.section, indexPath.row)
        if isinstance(value, TableViewCell):
            return value.native
        elif isinstance(value, dict):
            pass

        cellstyle = value.get('style', 'default')
        if cellstyle == 'subtitle':
            cell = tableView.dequeueReusableCellWithIdentifier_("row")
            if cell is None:
                cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleSubtitle, "rowsub")
                cell.textLabel.text = value.get('title', 'error')
                cell.detailTextLabel.text = value.get('subtitle', ' ')
                cell.detailTextLabel.font = UIFont.fontWithName('Menlo', size=14)
                if value.get('content', None):
                    if hasattr(value['content'], 'native'):
                        cell.contentView.addSubview(value['content'].native)

        elif cellstyle == 'value1':
            cell = tableView.dequeueReusableCellWithIdentifier_("row")
            if cell is None:
                cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleValue1, "rowv2")
                cell.textLabel.text = value.get('title', 'error')
                if value.get('subtitle', None):
                    cell.detailTextLabel.text = value['subtitle']
                if value.get('content', None):
                    if hasattr(value['content'], 'native'):
                        cell.contentView.addSubview(value['content'].native)

        elif cellstyle == 'value2':
            cell = tableView.dequeueReusableCellWithIdentifier_("row")
            if cell is None:
                cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleValue2, "rowv1")
                cell.textLabel.text = value.get('title', 'error')
                if value.get('subtitle', None):
                    cell.detailTextLabel.text = value['subtitle']
                if value.get('content', None):
                    if hasattr(value['content'], 'native'):
                        cell.contentView.addSubview(value['content'].native)

        else:
            cell = tableView.dequeueReusableCellWithIdentifier_("row")
            if cell is None:
                cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleDefault, "row1")
                cell.textLabel.text = value.get('title', 'error')
                if value.get('content', None):
                    if hasattr(value['content'], 'native'):
                        cell.contentView.addSubview(value['content'].native)

                if value['subtitle'] == 'grayx':
                    dprint('gray cell')
                    backgroundConfig = UIBackgroundConfiguration.listPlainCellConfiguration()
                    backgroundConfig.tintColor = UIColor.grayColor
                    cell.backgroundConfiguration = backgroundConfig


        if value.get('accessory', None):
            value['accessory_type'] = value['accessory']

        accessory_type = value.get('accessory_type', None)
        if accessory_type == 'disclosure_indicator':
            cell.accessoryType = 1
        elif accessory_type == 'detail_disclosure_button':
            cell.accessoryType = 2
        elif accessory_type == 'checkmark':
            cell.accessoryType = 3
        elif accessory_type == 'detail_button':
            cell.accessoryType = 4
        else:
            pass

        img = value.get('image', None)
        if isinstance(img, ObjCInstance):
            if img.description[1:9] == 'UIImage:':
                cell.imageView.image = img

        if value.get('text_color', None):
            ncolor = uicolor(value['text_color'])
            if ncolor:
                cell.textLabel.textColor = ncolor
                if value['style'] == 'subtitle':
                    cell.detailTextLabel.textColor = ncolor

        if isinstance(value.get('font', None), tuple):
            cell.textLabel.font = Font.named(value['font'])

        if isinstance(value.get('number_of_lines', None), int):
            cell.textLabel.numberOfLines = value['number_of_lines']

        if value.get('highlight_color', None):
            bgview = View()
            bgview.background_color = value['highlight_color']
            cell.selectedBackgroundView = bgview.native

        if indexPath.row == -1:
            dprint('row 0')
            for key in cell.objc_class.instance_method_ptrs.keys():
                if 'will' in key:
                    dprint(key)

        return cell

    def tableview_cell_for_row(self, tableview, section, row):
        item = self.data[row]
        if isinstance(item, str):
            dprint(str)
            return {'title': str(item), 'subtitle': '', 'style': 'default', 'accessory': 'none'}
        elif isinstance(item, dict):
            return {'title': item.get('title', 'error'),
                    'subtitle': item.get('subtitle', ''),
                    'style': item.get('style', 'default'),
                    'image': item.get('image', None),
                    'accessory_type': item.get('accessory_type', 'none')
            }
        """
        'text_color': self.text_color,
        'font': self.font,
        'number_of_lines': self.number_of_lines,
        'highlight_color': self.highlight_color
        """

    def tableview_height_for_row(self, tableview, section, row):
        return -1

    def tableview_title_for_header(self, tv, section):
        dprint('-- section title --')
        return ''

    def tableview_can_delete(self, tableview, section, row):
        return self.delete_enabled

    def tableview_delete(self, tableview, section, row):
        dprint('delete:', row)
        self.begin_updates()
        self.data.pop(row)
        self.delete_rows([(row)])
        self.end_updates()
        if self.edit_action:
            self.edit_action(self)

    def tableview_can_edit(self, tableview, section, row):
        if self.delete_enabled or self.move_enabled:
            return True
        else:
            return False

    def tableview_can_move(self, tableview, section, row):
        return self.move_enabled

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        dprint(from_row, to_row)
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
        dprint('moved')

    def tableview_editing_style(self, tableview, section, row):
        if self.tableview_can_delete(tableview, section, row):
            return UITableViewCellEditingStyleDelete
        else:
            return UITableViewCellEditingStyleNone

    def tableview_context_menu(self, tableview, row):
        if self.menu_items is None:
            return None
        if len(self.menu_items) == 0:
            return None
        self.lastrow = row
        self.menublock = Block(self.create_menu, objc_id, (objc_id))
        menuconfig = UIContextMenuConfiguration.configurationWithIdentifier(str(row), previewProvider=None, actionProvider=self.menublock)
        return menuconfig

    def tableview_did_select(self, tableview, section, row):
        dprint('selelcted: ', row)
        if self.action:
            self.action(self)

    def tableview_did_deselect(self, tableview, section, row):
        dprint('deselelcted: ', row)

    def tableview_title_for_delete_button(self, tableview, section, row):
        return 'Delete'

    def tableview_accessory_button_tapped(self, tableview, section, row):
        dprint('accessory tapped: ', row)
        if self.accessory_action:
            self.accessory_action(self)

    def reload(self):
        self.native.reloadData()

    def reload_data(self):
        self.native.reloadData()

    def delete_rows(self, rows):
        items = []
        #self.native.beginUpdates()
        for row in rows:
            dprint('delete', row)
            if type(row) is tuple:
                rownum = row[1]
                section = row[0]
                index_path = NSIndexPath.indexPathForRow(rownum, inSection=section)
            elif type(row) is int:
                index_path = NSIndexPath.indexPathForRow(row, inSection=0)
            items.append(index_path)

        self.native.deleteRowsAtIndexPaths(ns_from_py(items), withRowAnimation=True)
        #self.native.endUpdates()
        dprint('delete ok')

    def insert_rows(self, rows):
        items = []
        self.native.beginUpdates()
        for row in rows:
            dprint('delete', row)
            if type(row) is tuple:
                rownum = row[1]
                section = row[0]
                index_path = NSIndexPath.indexPathForRow(rownum, inSection=section)
            elif type(row) is int:
                index_path = NSIndexPath.indexPathForRow(row, inSection=0)
            items.append(index_path)

        self.native.insertRowsAtIndexPaths(ns_from_py(items), withRowAnimation=True)
        self.native.endUpdates()
        dprint('insert ok')

    def get_cell(self, section, row):
        index_path = NSIndexPath.indexPathForRow(row, inSection=section)
        dprint(index_path)
        cell = self.native.cellForRowAtIndexPath_(index_path)
        dprint(cell.accessoryType)
        if cell.accessoryType == 0:
            cell.accessoryType = 3
        else:
            cell.accessoryType = 0
        return cell.accessoryType

    @property
    def refresh_action(self):
        return None

    @refresh_action.setter
    def refresh_action(self, handler: callable or None) -> None:
        dprint('set refresh action')
        if callable(handler):
            self.refresh_handler = handler
            self.controller.refreshControl = UIRefreshControl.alloc().init()
            self.controller.refreshControl.addTarget(self.controller,
                action=SEL('onRefresh:'),
                forControlEvents=UIControlEventValueChanged
            )
        else:
            if self.controller.refreshControl:
                self.controller.refreshControl.removeFromSuperview()
            self.controller.refreshControl = None

    @property
    def search_action(self):
        return None

    @search_action.setter
    def search_action(self, handler: callable or None) -> None:
        if callable(handler):
            dprint('set search handler')
            self.search_handler = handler
            self.searchController = UISearchController.alloc().initWithSearchResultsController_(None)
            self.searchController.searchResultsUpdater = self.controller
            self.searchController.obscuresBackgroundDuringPresentation = False
            self.searchController.searchBar.placeholder = 'enter search'
            self.searchController.searchBar.autocapitalizationType = 0
            self.controller.navigationItem.searchController = self.searchController
            send_message(
                self.searchController.searchBar,
                'setAutocapitalizationType:',
                0,
                restype=None,
                argtypes=[c_int]
            )
        else:
            if self.controller.searchController:
                self.controller.searchController.removeFromSuperview()
            self.controller.searchController = None

    def scroll_to_row(self, row):
        self.native.scrollToRowAtIndexPath(
            NSIndexPath.indexPathForRow(row, inSection=0),
            atScrollPosition=UITableViewScrollPositionNone,
            animated=False
        )

