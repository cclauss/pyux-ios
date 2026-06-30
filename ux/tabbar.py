from rubicon.objc import CGSize

from .core import asyncq, topvc
from .uikit import UIColor, UITabBarController


class TabBar():

    def __init__(self):
        self.controller = UITabBarController.alloc().init()
        self.controller.interface = self
        self.native = self.controller.view
        self.controller.view.backgroundColor = UIColor.systemBackgroundColor()

    def set_views(self, views):
        controllers = []
        from .navigationview import get_vc
        for view in views:
            if not view.controller:
                vcclass = get_vc()
                view.controller = vcclass.alloc().init()
                view.controller.interface = view
                view.controller.view.addSubview(view.native)

            controllers.append(view.controller)

        def setvcs(_self):
            self.controller.setViewControllers(controllers, animated=True)

        asyncq(setvcs)

    def present(self, style='sheet'):
        if style == 'fullscreen':
            self.controller.setModalPresentationStyle_(0)
        else:
            self.controller.setModalPresentationStyle_(2)

        self.controller.preferredContentSize = CGSize(580, 800)
        top = topvc()

        def _present(_self):
            top.presentViewController_animated_completion_(self.controller, True, None)

        asyncq(_present)

    def close(self, sender=None):
        self.controller.dismissViewControllerAnimated_completion_(True, None)

