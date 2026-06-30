from rubicon.objc import Block, ObjCInstance
from rubicon.objc.runtime import objc_id

from .uikit import UIAction, UIMenu


class Action:

    def __init__(self,
        title,
        handler,
        image=None,
        attributes=None,
        state=False,
        discoverability_title=None,
    ):
        self._menu = None
        self._handler = handler
        self._title = title
        self._image = image
        self._attributes = attributes
        self._state = state
        self._discoverability_title = discoverability_title
        self.native = None
        self.create_action()

    def action_handler(self, sender) -> None:
        self._handler(ObjCInstance(sender))

    def create_action(self):
        handler_block=Block(self.action_handler, None, objc_id)
        self.native  = UIAction.actionWithHandler_(handler_block)
        self.native.title = self._title
        if self._image:
            self.native.setImage(self._image)
        if self._attributes:
            self.native.setAttributes(self._attributes)

class Menu:

    def __init__(self, title='Actions', items=None):
        self.title = title
        self.items = items
        self.handlers = {}
        self.create_menu(self.title, self.items)

    def new_action(self, actdict):
        return Action(
            actdict.get('title', None),
            actdict.get('handler', None),
            actdict.get('image', None),
            actdict.get('attributes', None)
        )

    def menu_action(self, sender) -> None:
        title = ObjCInstance(sender).title
        action_handler = self.handlers[str(title)]
        action_handler(ObjCInstance(sender))

    def create_menu(self, title, items):
        menuactions = []
        for item in items:
            if isinstance(item, dict):
                menu_action = self.new_action(item).native
            else:
                if isinstance(item[1], list):
                    menu_action = self.create_menu(item[0], item[1])
                else:
                    menu_handler_block=Block(self.menu_action, None, objc_id)
                    menu_action = UIAction.actionWithHandler_(menu_handler_block)
                    menu_action.title = item[0]
                    self.handlers[item[0]] = item[1]
            if menu_action:
                menuactions.append(menu_action)
        menu_action = UIAction.actionWithHandler_(None)
        menu_action.title = ' '
        menuactions.append(menu_action)

        self.native = UIMenu.menuWithTitle(str(title), children=menuactions)
        return self.native
