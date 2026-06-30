from threading import current_thread

from rubicon.objc import CGPoint, CGRect, CGSize, ObjCInstance

from .colors import uicolor, uicolor_rgba
from .core import asyncq, convert_rect, dprint, topvc, waitModal, will_block
from .uikit import UIColor

UIViewAutoresizingNone = 0
UIViewAutoresizingFlexibleLeftMargin = 1 << 0
UIViewAutoresizingFlexibleWidth = 1 << 1
UIViewAutoresizingFlexibleRightMargin = 1 << 2
UIViewAutoresizingFlexibleTopMargin = 1 << 3
UIViewAutoresizingFlexibleHeight = 1 << 4
UIViewAutoresizingFlexibleBottomMargin = 1 << 5

class ViewCore():

    def init(self):
        self._name = None
        self.controller = None
        self.left_items = False
        self.right_items = False
        self.modal = None

    def viewattrs(self, arg, value):
        if arg == 'name':
            self.name = value
            return True
        if arg == 'alpha':
            pass
        if arg == 'background_color':
            self.background_color = value
            return True
        if arg == 'border_color':
            pass
        if arg == 'border_width':
            pass
        if arg == 'corner_radius':
            pass
        if arg == 'flex':
            self.flex = value
            return True
        if arg == 'frame':
            self.frame = value
            return True
        return False

    def add_subview(self, content):
        self.native.addSubview(content.native)

    @property
    def background_color(self) -> UIColor:
        color = self.native.backgroundColor
        return uicolor_rgba(color)

    @background_color.setter
    def background_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.native.backgroundColor = ncolor

    @property
    def bg_color(self) -> UIColor:
        color = self.native.backgroundColor
        return uicolor_rgba(color)

    @bg_color.setter
    def bg_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.native.backgroundColor = ncolor

    @property
    def border_color(self):
        color = UIColor.colorWithCGColor(self.native.layer.borderColor)
        return uicolor_rgba(ObjCInstance(color))

    @border_color.setter
    def border_color(self, color):
        ncolor = uicolor(color)
        dprint('ncolor', ncolor)
        if ncolor:
            self.native.layer.borderColor = UIColor(ncolor).CGColor

    @property
    def border_width(self):
        return self.native.layer.borderWidth

    @border_width.setter
    def border_width(self, value):
        self.native.layer.borderWidth = value

    @property
    def bounds(self):
        return (self.native.bounds.origin.x,
                self.native.bounds.origin.y,
                self.native.bounds.size.width,
                self.native.bounds.size.height)

    def bring_to_front(self, content):
        dprint('bring_to_front')
        self.native.bringSubviewToFront_(content.native)

    @property
    def center(self):
        return (self.native.center.x, self.native.center.y)

    @center.setter
    def center(self, value):
        self.native.center = CGPoint(value[0], value[1])

    def close(self, sender=None):
        self.controller.dismissViewControllerAnimated_completion_(True, None)

    def convert_rect(self, frame, from_view=None, to_view=None):
        fx, fy, fw, fh = frame
        rect = CGRect(CGPoint(fx, fy), CGSize(fh, fy))
        if from_view:
            newrect = self.native.convertRect(rect, fromView=from_view.native)
            return (newrect.origin.x,
                newrect.origin.y,
                newrect.size.width,
                newrect.size.height)
        elif to_view:
            newrect = self.native.convertRect(rect, toView=to_view.native)
            return (newrect.origin.x,
                newrect.origin.y,
                newrect.size.width,
                newrect.size.height)
        else:
            return (0, 0, 400, 0)

    @property
    def corner_radius(self):
        return self.native.layer.cornerRadius

    @corner_radius.setter
    def corner_radius(self, value):
        self.native.layer.cornerRadius = value

    def ensure_vc(self):
        if not self.controller:
            from .navigationview import get_vc
            vcclass = get_vc()
            self.controller = vcclass.alloc().init()
            self.controller.interface = self
            self.controller.view.addSubview(self.native)

    @property
    def flex(self):
        flexstr = ''
        mask = self.native.autoresizingMask
        if mask & UIViewAutoresizingFlexibleLeftMargin > 0:
            flexstr += 'L'
        if mask & UIViewAutoresizingFlexibleWidth > 0:
            flexstr += 'W'
        if mask & UIViewAutoresizingFlexibleRightMargin > 0:
            flexstr += 'R'
        if mask & UIViewAutoresizingFlexibleTopMargin > 0:
            flexstr += 'T'
        if mask & UIViewAutoresizingFlexibleHeight > 0:
            flexstr += 'H'
        if mask & UIViewAutoresizingFlexibleBottomMargin > 0:
            flexstr += 'B'
        return flexstr

    @flex.setter
    def flex(self, flexstr):
        mask = 0
        if 'L' in flexstr:
            mask += UIViewAutoresizingFlexibleLeftMargin
        if 'W' in flexstr:
            mask += UIViewAutoresizingFlexibleWidth
        if 'R' in flexstr:
            mask += UIViewAutoresizingFlexibleRightMargin
        if 'T' in flexstr:
            mask += UIViewAutoresizingFlexibleTopMargin
        if 'H' in flexstr:
            mask += UIViewAutoresizingFlexibleHeight
        if 'B' in flexstr:
            mask += UIViewAutoresizingFlexibleBottomMargin

        self.native.autoresizingMask = mask

    @property
    def frame(self):
        return (self.native.frame.origin.x,
                self.native.frame.origin.y,
                self.native.frame.size.width,
                self.native.frame.size.height)

    @frame.setter
    def frame(self, frameset):
        x, y, w, h = frameset
        def _setframe(_self):
            self.native.frame = CGRect(CGPoint(x,y), CGSize(w, h))

        self.native.frame = CGRect(CGPoint(x,y), CGSize(w, h))

    @property
    def height(self):
        return self.native.frame.size.height

    @height.setter
    def height(self, value):
        frame = self.native.frame
        frame.size.height = value
        self.native.frame = frame

    @property
    def left_button_items(self):
        dprint('left')
        if self.left_items:
            return True
        return False

    @left_button_items.setter
    def left_button_items(self, btnitems):
        self.ensure_vc()
        dprint('vc left items')
        leftitems = []
        for item in btnitems:
            leftitems.append(item.native)
        def _setitems(_self):
            self.controller.navigationItem.leftBarButtonItems = leftitems
        self.left_items = True
        asyncq(_setitems)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, title):
        self._name = title

    @property
    def navigation_view(self):
        return self.controller.navigationController.interface
        try:
            return self.controller.navigationController.interface
        except Exception:

            return None

    def present(self, style='sheet', animated=True, popover_item=None,
            popover_location=None, hide_title_bar=False,
            title_bar_color=None, title_color=None, orientations=None,
            hide_close_button=False, right_close_button=False):

        from .navigationview import NavigationView, get_vc
        if not self.controller:
            vcclass = get_vc()
            self.controller = vcclass.alloc().init()
            self.controller.interface = self
            if self.name:
                self.controller.navigationItem.title = self.name
            self.controller.view.addSubview(self.native)

        if hide_title_bar:
            if not style == 'fullscreen':
                x, y, w, h = self.frame

            if style == 'sheet':
                self.controller.setModalPresentationStyle_(2)
            elif style == 'fullscreen':
                self.controller.setModalPresentationStyle_(0)
            elif style == 'popover':
                self.controller.setModalPresentationStyle_(2)
            else:
                self.controller.setModalPresentationStyle_(6)

            top = topvc()

            def _present(_self):
                top.presentViewController_animated_completion_(self.controller, animated, None)

            asyncq(_present)

        else:

            def navpresent():
                dprint('navpresent', current_thread().name)
                nv = NavigationView(self)
                nv.present(style=style, animated=animated, popover_item=popover_item,
                    popover_location=popover_location, hide_title_bar=False,
                    title_bar_color=title_bar_color, title_color=title_color,
                    orientations=None, hide_close_button=hide_close_button,
                    right_close_button=right_close_button)

            navpresent()

    @property
    def objc_instance(self):
        return self.native

    def remove_subview(self, view):
        view.native.removeFromSuperview()

    @property
    def right_button_items(self):
        dprint('right')
        if self.right_items:
            return True
        return False

    @right_button_items.setter
    def right_button_items(self, btnitems):
        self.ensure_vc()
        dprint('vc right items')
        rightitems = []
        for item in btnitems:
            rightitems.append(item.native)
        def _setitems(_self):
            self.controller.navigationItem.rightBarButtonItems = rightitems
        self.right_items = True
        asyncq(_setitems)

    def size_to_fit(self):
        self.native.sizeToFit()

    @property
    def superview(self):
        if self.native.superview():
            return self.native.superview().interface
        return None

    @property
    def subviews(self):
        views = []
        for view in self.native.subviews():
            try:
                views.append(view.interface)
            except Exception:
                dprint('type err', view)

        return tuple(views)

    def wait_modal(self):
        if will_block(None):
            return None

        self.modal = waitModal()
        self.modal.wait()

    @property
    def width(self):
        return self.native.frame.size.width

    @width.setter
    def width(self, value):
        frame = self.native.frame
        frame.size.width = value
        self.native.frame = frame

    @property
    def x(self):
        return self.native.frame.origin.x

    @x.setter
    def x(self, value):
        frame = self.native.frame
        frame.origin.x = value
        self.native.frame = frame

    @property
    def y(self):
        return self.native.frame.origin.y

    @y.setter
    def y(self, value):
        frame = self.native.frame
        frame.origin.y = value
        self.native.frame = frame

    @property
    def tabbar_item(self):
        self.ensure_vc()
        return self.controller.tabBarItem

    @property
    def tag(self):
        return self.native.tag

    @tag.setter
    def tag(self, value):
        self.native.tag = value

    def did_load(self):
        dprint('--- viewDidLoad ---')
        dprint(self.frame)

    def keyboard_will_show(self, notification):
        from .textview import TextView
        kbrect = notification.userInfo.objectForKey('UIKeyboardFrameEndUserInfoKey').CGRectValue
        kbframe = (kbrect.origin.x, kbrect.origin.y, kbrect.size.width, kbrect.size.height)

        if kbrect.size.height > 0:
            for sv in self.subviews:
                if isinstance(sv, TextView):
                    dprint(type(sv))
                    if sv._auto_content_inset:
                        tx, ty, tw, th = sv.frame
                        r = convert_rect(kbframe, to_view=self)
                        dprint('sv', sv.height)
                        dprint(r)
                        h = round(ty + th - r[1],2)
                        if h < 0:
                            h = 0
                        dprint('kbh', h)
                        sv.content_inset = (0, 0, h, 0)

            self.keyboard_will_change(kbframe)

    def keyboard_will_hide(self, notification):
        from .textview import TextView
        kbrect = notification.userInfo.objectForKey('UIKeyboardFrameEndUserInfoKey').CGRectValue
        kbframe = (kbrect.origin.x, kbrect.origin.y, kbrect.size.width, kbrect.size.height)

        for sv in self.subviews:
            if isinstance(sv, TextView):
                if sv._auto_content_inset:
                    dprint(type(sv))
                    dprint('kbh', 0)
                    sv.content_inset = (0, 0, 0, 0)

        self.keyboard_will_change(kbframe)

    def keyboard_will_change(self, kbframe):
        dprint('-- keyboardWillChange --', self)

    def _insets_changed(self):
        dprint('-- viewInsetsChanged --')
        self.insets_changed()

    def insets_changed(self):
        super = self.native.superview()
        if super:
            self.native.frame = super.safeAreaLayoutGuide.layoutFrame

    def will_layout(self):
        dprint('-- viewWillLayout --', self)
        self.layout()

    def did_layout(self):
        dprint('-- viewDidLayout --')

    def layout(self):
        dprint('layout')

    def will_appear(self, sender):
        dprint('--- viewWillAppear ---')
        self.native.frame = sender.view.safeAreaLayoutGuide.layoutFrame

    def did_appear(self):
        dprint('-- view did appear --', self)

    def will_close(self):
        dprint('-- view will close --')

    def _did_close(self):
        dprint('-- view-did-close --')
        if self.modal:
            self.modal.set_result(None)
            self.modal = None
        self.did_close()

    def did_close(self):
        pass


