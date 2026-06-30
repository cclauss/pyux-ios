from rubicon.objc import Block
from rubicon.objc.runtime import objc_id

from .menu import Menu
from .uikit import (
    UIAction,
    UIBarButtonItem,
    UIBarButtonSystemItem,
)


class ButtonItem():
    def __init__(self, title=None, image=None, action=None, menu=None, enabled=True, tint_color=None):
        self.action_handler = None
        if action:
            self.action = action
            item_handler_block=Block(self._action, None, objc_id)
            item_action = UIAction.actionWithHandler_(item_handler_block)
        else:
            item_action = None

        if isinstance(image, str):
            self.native = UIBarButtonItem.alloc().initWithBarButtonSystemItem_primaryAction_(
                self.sysimage(image),
                item_action
            )
        else:
            self.native = UIBarButtonItem.alloc().initWithPrimaryAction(item_action)
            if title:
                self.native.setTitle(title)
            elif image:
                self.native.setImage(image)

        if isinstance(menu, Menu):
            self.native.menu = menu.native

    def _action(self, sender):
        if self.action_handler:
            self.action_handler(self)

    @property
    def action(self):
        return self.action_handler

    @action.setter
    def action(self, handler):
        if callable(handler):
            self.action_handler = handler

    @property
    def menu(self):
        return self.native.menu

    @menu.setter
    def menu(self, menu):
        self.native.menu = menu.native

    def sysimage(self, sysbutton):
        if sysbutton == 'done':
            return UIBarButtonSystemItem.Done
        if sysbutton == 'menu':
            return UIBarButtonSystemItem.Organize
        print('sysbutton', sysbutton)
        return UIBarButtonSystemItem.Organize

    @property
    def title(self):
        return self.native.title

    @title.setter
    def title(self, title):
        self.native.setTitle(title)
