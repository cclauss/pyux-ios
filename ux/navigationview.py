import time

from rubicon.objc import (
    SEL,
    CGPoint,
    CGRect,
    CGSize,
    ObjCClass,
    ObjCInstance,
    ns_from_py,
    objc_method,
    py_from_ns,
    send_super,
)
from rubicon.objc.runtime import get_class

from .buttonitem import ButtonItem
from .colors import uicolor
from .core import asyncq, dprint, in_background, topvc, uxviews
from .foundation import NSNotificationCenter
from .image import Image
from .navigationbar import NavigationBar, NavigationItem
from .tabbar import TabBar
from .uikit import (
    NSForegroundColorAttributeName,
    NSLayoutConstraint,
    UIColor,
    UIKeyboardWillHideNotification,
    UIKeyboardWillShowNotification,
    UINavigationController,
    UIViewController,
)
from .view import View


def get_vc():
    if get_class('uxViewController').value is not None:
        return ObjCClass(get_class('uxViewController'))
    else:
        class uxViewController(UIViewController):
            @objc_method
            def viewDidLoad(self) -> None:
                send_super(__class__, self, "viewDidLoad")
                self.interface.did_load()

            @objc_method
            def viewWillAppear_(self) -> None:
                NSNotificationCenter.defaultCenter.addObserver(
                    self,
                    selector=SEL('keyboardWillShow:'),
                    name=UIKeyboardWillShowNotification,
                    object=None
                )
                NSNotificationCenter.defaultCenter.addObserver(
                    self,
                    selector=SEL('keyboardWillHide:'),
                    name=UIKeyboardWillHideNotification,
                    object=None
                )
                self.interface.will_appear(self)

            @objc_method
            def viewSafeAreaInsetsDidChange(self) -> None:
                send_super(__class__, self, "viewSafeAreaInsetsDidChange")
                self.interface._insets_changed()

            @objc_method
            def viewWillLayoutSubviews(self) -> None:
                send_super(__class__, self, "viewWillLayoutSubviews")
                self.interface.will_layout()

            @objc_method
            def viewDidLayoutSubviews(self) -> None:
                send_super(__class__, self, "viewDidLayoutSubviews")
                self.interface.did_layout()

            @objc_method
            def viewDidAppear_(self, animated: bool) -> None:
                self.interface.did_appear()

            @objc_method
            def viewWillDisappear_(self) -> None:
                NSNotificationCenter.defaultCenter.removeObserver(
                    self,
                    name=UIKeyboardWillShowNotification,
                    object=None
                )
                NSNotificationCenter.defaultCenter.removeObserver(
                    self,
                    name=UIKeyboardWillHideNotification,
                    object=None
                )
                self.interface.will_close()

            @objc_method
            def viewDidDisappear_(self, animated: bool) -> None:
                self.interface.ispresented = False
                self.interface._did_close()

            @objc_method
            def keyboardWillShow_(self, notification) -> None:
                self.interface.keyboard_will_show(notification)

            @objc_method
            def keyboardWillHide_(self, notification) -> None:
                self.interface.keyboard_will_hide(notification)

        return uxViewController

def get_nav():
    if get_class('uxNavController').value is not None:
        return ObjCClass(get_class('uxNavController'))
    else:
        class uxNavController(UINavigationController):

            @objc_method
            def viewDidLoad(self) -> None:
                send_super(__class__, self, "viewDidLoad")
                dprint('NAV view loaded')

        return uxNavController


class NavigationView():

    def __init__(self, view):
        def _init(_self):
            self.controller = navclass.alloc().initWithRootViewController_(vc)
            self.controller.interface = self
            self.controller.title = 'navapp'
            self.controller.retain()
            self.native = vc.view

        self.controller = None
        if view.controller:
            vc = view.controller
            vc.view.backgroundColor = UIColor.systemBackgroundColor()
            dprint('old vc')
            vc.interface = view
            dprint('navview')
            dprint(view.controller)
            self.container = vc.view
            self.view = view
        else:
            vcclass = get_vc()
            vc = vcclass.alloc().init()
            view.controller = vc
            vc.interface = view
            vc.view.addSubview(view.native)
            vc.view.backgroundColor = UIColor.systemBackgroundColor()
            dprint('new vc')
            self.container = vc.view
            self.view = view

        if isinstance(view, TabBar):
            print('TabBar can not be assigned NavigationView')
            return None

        if hasattr(view, 'name'):
            self.name = view.name
            view.controller.navigationItem.title = view.name
        else:
            self.name = None

        if not self.view.name:
            self.view.name = 'Hello Bosco'

        navclass = get_nav()
        asyncq(_init)

    def close(self, sender):
        dprint("dismiss nav")
        self.controller.dismissViewControllerAnimated_completion_(True, None)
        self.controller.release()
        dprint('done')
        return

    def left_button_items(self):
        dprint('left nav')
        imgx = Image.named('system:xmark')
        btnx = ButtonItem(image=imgx, action=self.close)
        leftitems = [btnx.native]
        dprint(self.view.left_button_items)
        if self.view.left_button_items:
            for item in self.view.controller.navigationItem.leftBarButtonItems:
                leftitems.append(item)
        self.view.controller.navigationItem.leftBarButtonItems = leftitems

    def right_button_items(self):
        dprint('right nav')
        imgx = Image.named('system:xmark')
        btnx = ButtonItem(image=imgx, action=self.close)
        rightitems = [btnx.native]
        if self.view.right_button_items:
            for item in self.view.controller.navigationItem.rightBarButtonItems:
                rightitems.append(item)
        self.view.controller.navigationItem.rightBarButtonItems = rightitems

    def layout(self):
        dprint('layout')

    def printobj(self, obj):
        if isinstance(obj, ObjCInstance):
            _repr = str(obj.debugDescription)
            val = {
                "Description": _repr,
                "Superclass": str(obj.superclass.name),
                "Title": py_from_ns(obj.title),
                #"Methods": str(obj._methodDescription()),
            }
            print(val)
        else:
            print('unknown')

    @in_background
    def present(self, style='sheet', animated=True, popover_item=None,
            popover_location=None, hide_title_bar=False, title_bar_color=None,
            title_color=None, orientations=None, hide_close_button=False,
            right_close_button=False, topbar=False, title=None, vc=None):

        def _present(_self):
            top = topvc()
            hide_close_btn = hide_close_button

            if not topbar:

                textAttributes = {}

                if title_bar_color:
                    ncolor = uicolor(title_bar_color)
                    if ncolor:
                        dprint(ncolor)
                        self.container.backgroundColor = ncolor
                        self.controller.navigationBar.barTintColor = ncolor
                else:
                    ncolor = UIColor.systemBackgroundColor()
                    if ncolor:
                        dprint(ncolor)
                        self.controller.navigationBar.barTintColor = ncolor

                if title_color:
                    ncolor = uicolor(title_color)
                    if ncolor:
                        dprint(ncolor)
                        textAttributes[str(NSForegroundColorAttributeName)] = ncolor
                        self.controller.navigationBar.setTitleTextAttributes(ns_from_py(textAttributes))

                if style == 'popover':
                    hide_close_btn = True

                if not hide_close_btn:
                    if right_close_button:
                        self.right_button_items()
                    else:
                        self.left_button_items()

                dprint(self.view.native.traitCollection)

                if style == 'fullscreen':
                    self.controller.setModalPresentationStyle_(0)
                elif style == 'popover':
                    dprint('------------ popover -----------')
                    self.controller.setModalPresentationStyle_(7)
                    dprint(popover_location)
                    dprint(top.interface.native)
                    x, y, w, h = self.view.frame
                    self.controller.preferredContentSize = CGSize(w, h)
                    if popover_item:
                        self.controller.popoverPresentationController().sourceItem = popover_item.native
                    else:
                        x, y = popover_location
                        self.controller.popoverPresentationController().sourceView = top.interface.native
                        self.controller.popoverPresentationController().sourceRect = CGRect(CGPoint(0, 0), CGSize(x, y))
                elif style == 'sheet':
                    x, y, w, h = self.view.frame
                    dprint(style, self.view.frame)
                    self.controller.preferredContentSize = CGSize(w, h)
                    self.controller.setModalPresentationStyle_(2)
                else:
                    x, y, w, h = self.view.frame
                    dprint(style, self.view.frame)
                    self.controller.preferredContentSize = CGSize(w, h)
                    self.controller.setModalPresentationStyle_(-2)
                top.presentViewController_animated_completion_(self.controller, animated, None)
            else:
                dprint('topbar')

                nbview = View()
                nbview.name = '-topview'
                nbview.frame = (0, 0, 580, 620)
                nbview.flex = 'WH'
                uxviews.append(nbview)

                vcclass = get_vc()
                nbview.controller = vcclass.alloc().init()
                nbview.controller.interface = nbview
                nbview.controller.view.addSubview(nbview.native)
                nbview.native.setTranslatesAutoresizingMaskIntoConstraints_(True)

                img = Image.named('system:xmark')
                btnclose = ButtonItem(image=img, action=nbview.close)
                navbar = NavigationBar()
                if title_bar_color:
                    dprint('title_bar_color', title_bar_color)
                    navbar.bar_color = title_bar_color
                if title_color:
                    navbar.tint_color = title_color

                headerView = navbar
                title1 = NavigationItem(title=title)
                headerView.items = [title1]

                if not hide_close_btn:
                    img = Image.named('system:xmark')
                    btnclose = ButtonItem(image=img, action=nbview.close)
                    if right_close_button:
                        title1.right_button_items = [btnclose]
                    else:
                        title1.left_button_items = [btnclose]

                ncolor = uicolor('green')
                nbview.navbar = headerView
                nbview.present_style = style
                dprint('header', headerView)

                vcclass = get_vc()
                navbar.controller = vcclass.alloc().init()
                navbar.controller.interface = nbview
                navbar.controller.view.addSubview(navbar.native)
                nbview.add_subview(navbar)

                nbsuper = navbar.native
                nbsuper.setTranslatesAutoresizingMaskIntoConstraints_(False)
                dprint('nbview', nbview.native)
                dprint(nbview.native.leftAnchor)
                dprint('nbsuper', nbsuper)
                dprint(nbsuper.leftAnchor)

                nbview.controller.view.addSubview(nbview.native)
                self.controller.navigationBar.autoresizingMask = 1 << 1
                self.controller.willMoveToParentViewController_(nbview.controller)
                nbview.native.addSubview(self.controller.view)
                self.controller.didMoveToParentViewController_(nbview.controller)
                self.controller.navigationBar.topItem.title = ''
                self.controller.navigationBar.topItem.rightBarButtonItems = None
                dprint(self.controller.navigationBar)
                self.controller.view.setTranslatesAutoresizingMaskIntoConstraints_(False)
                dprint('*********', self.controller.view)
                dprint(self.native.constraints())
                dprint('done')

                NSLayoutConstraint.activateConstraints_([
                    nbsuper.leftAnchor.constraintEqualToAnchor_(
                        nbview.native.leftAnchor),
                    nbsuper.rightAnchor.constraintEqualToAnchor_(
                        nbview.native.rightAnchor),
                    nbsuper.topAnchor.constraintEqualToAnchor_(
                        nbview.native.topAnchor)
                ])

                NSLayoutConstraint.activateConstraints_([
                    self.controller.view.leftAnchor.constraintEqualToAnchor_(
                        nbview.native.leftAnchor),
                   self.controller.view.rightAnchor.constraintEqualToAnchor_(
                        nbview.native.rightAnchor),
                    self.controller.view.topAnchor.constraintEqualToAnchor_(
                        navbar.native.bottomAnchor),
                    self.controller.view.bottomAnchor.constraintEqualToAnchor_(
                        nbview.native.bottomAnchor)
                ])
                if style == 'fullscreen':
                    nbview.controller.setModalPresentationStyle_(0)
                else:
                    x, y, w, h = nbview.frame
                    dprint(style, nbview.frame)
                    nbview.controller.preferredContentSize = CGSize(w, h)
                    nbview.controller.setModalPresentationStyle_(2)
                top.presentViewController_animated_completion_(nbview.controller, animated, None)

        for i in range(10):
            if self.controller:
                break
            time.sleep(.2)
            dprint('--- navwait ---', i)

        dprint('-ctrl-', self.controller)

        asyncq(_present)

    def push_view(self, content, animated=True):

        def _push_view(_self):
            if content.controller:
                dprint('has vc')
                if content.name:
                    content.controller.navigationItem.title = content.name

                ncolor = UIColor.systemBackgroundColor()
                if ncolor:
                    content.controller.view.backgroundColor = ncolor

                self.controller.pushViewController_animated_(content.controller, animated)
            else:
                dprint('needs vc')
                content.ensure_vc()
                if content.name:
                    content.controller.navigationItem.title = content.name

                content.controller.view.addSubview(content.native)
                content.controller.interface = content
                dprint(content.controller)
                ncolor = UIColor.systemBackgroundColor()
                if ncolor:
                    content.controller.view.backgroundColor = ncolor

                self.controller.pushViewController_animated_(content.controller, animated)

        asyncq(_push_view)

    def pop_view(self, animated=True):
        def _pop_view(_self):
            self.controller.popViewControllerAnimated_(animated)
        asyncq(_pop_view)
