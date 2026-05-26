from rubicon.objc import CGSize, ObjCClass, objc_method
from rubicon.objc.runtime import get_class
from .core import asyncq, get_window_size, topvc, uxviews
from .colors import *
from .tabbar import *

from .uikit import UIColor, UISplitViewController

def get_splitview():
    if get_class('uxSplitView').value is not None:
        return ObjCClass(get_class('uxSplitView'))
    else:
        class uxSplitView(UISplitViewController):

            @objc_method
            def splitViewController_willChangeToDisplayMode_(self, svr, displayMode: int) -> None:
                #print('displayMode : ', displayMode)
                pass

            @objc_method
            def splitViewController_topColumnForCollapsingToProposedTopColumn_(self, svr, proposedTopColumn: int) -> int:
                if self.interface.collapsing_top_column:
                    return self.interface.collapsing_top_column(proposedTopColumn)
                else:
                    return proposedTopColumn

        return uxSplitView

class SplitView():

    def __init__(self, style='double'):
        splitcls = get_splitview()
        if style == 2 or style == 'double':
            self.controller = splitcls.alloc().initWithStyle_(1) # 1 = 2 colunms
        else:
            self.controller = splitcls.alloc().initWithStyle_(2) # 2 = 3 colunms
        self.controller.interface = self
        self.native = self.controller.view
        self.controller.delegate = self.controller

    def set_view(self, view, column):

        colnum = self.column_int(column)

        if isinstance(view, TabBar):
            if colnum != 2:
                print('TabBar can not be assigned to primary or supplementary columns')
                return None

        def setvc(self_):
            self.controller.setViewController_forColumn_(view.controller, colnum)

        if colnum == 3:
            asyncq(setvc)
        else:
            if not view.controller:
                vcclass = get_vc()
                view.controller = vcclass.alloc().init()
                view.controller.interface = view
                view.controller.view.addSubview(view.native)

            view.controller.view.backgroundColor = UIColor.systemBackgroundColor()
            if view.name:
                view.controller.navigationItem.title = view.name

            if colnum == 2:
                self.detailvc = view.controller
            asyncq(setvc)

    def set_tabbar(self, ctrl, column):

        if column == 2:
            self.detailvc = ctrl.controller
        def setvc(self_):
            self.controller.setViewController_forColumn_(ctrl.controller, column)
        asyncq(setvc)

    def present(self, style):
        sw, sh = get_window_size()
        w = 1200 if sw > 800 else sw
        if style == 'fullscreen':
            self.controller.setModalPresentationStyle_(0)
        else:
            self.controller.setModalPresentationStyle_(2)

        self.controller.preferredContentSize = CGSize(w, 800)
        top = topvc()
        uxviews.append(top)
        uxviews.append(top)
        def _present(_self):
            top.presentViewController_animated_completion_(self.controller, True, None)

        asyncq(_present)

    def collapsing_top_column(self, proposed):
        return proposed

    def single_mode(self):
        self.controller.preferredDisplayMode = 1 # 0 = auto ; secondaryOnly = 1 ; oneBesideSecondary = 2
        # oneOverSecondary = 3 ; twoBesideSecondary = 4 ; twoOverSecondary = 5 ; twoDisplaceSecondary = 6
        self.controller.preferredBehavior = 1  # 0 = auto ; 1 = tile ; 2 = overlay ; 3 = displace
        self.controller.presentsWithGesture = False
        # remove sidebar button, make sidebar always appear !
        # presentsWithGesture = displayMode != .oneBesideSecondary
        self.controller.maximumPrimaryColumnWidth = 100

        self.controller.displayModeButtonVisibility = 2 ; # 0 = auto ;# 1 = always ;# 2 = never
        self.controller.showsSecondaryOnlyButton = False
        self.controller.collasped = True
        self.controller.hideColumn(0)
        self.controller.hideColumn(1)

    def show_column(self, column):
        self.controller.showColumn(self.column_int(column))

    def hide_column(self, column):
        self.controller.hideColumn(self.column_int(column))

    def show_primary(self, sender=None):
        self.controller.showColumn(0)

    def show_supplementary(self):
        self.controller.showColumn(1)

    def show_secordary(self):
        self.controller.showColumn(2)

    @property
    def collasped(self):
        return self.controller.isCollapsed()

    @property
    def display_mode(self):
        return self.controller.preferredDisplayMode

    @display_mode.setter
    def display_mode(self, value):
        self.controller.preferredDisplayMode = self.display_mode_int(value)

    @property
    def display_mode_button(self):
        return self.controller.displayModeButtonVisibility

    @display_mode_button.setter
    def display_mode_button(self, value):
        def set_async(cmd):
            self.controller.displayModeButtonVisibility = self.display_mode_btn_int(value)
        asyncq(set_async)

    @property
    def presents_with_gesture(self):
        return self.controller.presentsWithGesture

    @presents_with_gesture.setter
    def presents_with_gesture(self, value):
        self.controller.presentsWithGesture = value

    @property
    def secondary_only_button(self):
        return self.controller.showsSecondaryOnlyButton

    @secondary_only_button.setter
    def secondary_only_button(self, value):
        self.controller.showsSecondaryOnlyButton = value

    @property
    def split_behavior(self):
        return self.controller.preferredBehavior

    @split_behavior.setter
    def split_behavior(self, value):
        # 0 = auto ; 1 = tile ; 2 = overlay ; 3 = displace
        self.controller.preferredBehavior = self.split_behavior_int(value)

    def close(self, sender=None):
        self.controller.dismissViewControllerAnimated_completion_(True, None)

    def display_mode_int(self, value):
        if isinstance(value, int):
            if value < 0 or value > 6:
                return 0
            else:
                return value
        elif isinstance(value, str):
            if value == 'auto':
                return 0
            elif value == 'secondary_only' or value == 'secondaryOnly':
                return 1
            elif value == 'one_beside_secondary' or value == 'oneBesideSecondary':
                return 2
            elif value == 'one_over_secondary' or value == 'oneOverSecondary':
                return 3
            elif value == 'two_beside_secondary' or value == 'twoBesideSecondary':
                return 4
            elif value == 'two_over_secondary' or value == 'twoOverSecondary':
                return 5
            elif value == 'two_displace_secondary' or value == 'twoDisplaceSecondary':
                return 6
            else:
                return 0
        else:
            return 0

    def display_mode_btn_int(self, value):
        # 0 = auto ;# 1 = never ;# 2 = always
        if isinstance(value, int):
            if value < 0 or value > 2:
                return 0
            else:
                return value
        elif isinstance(value, str):
            if value == 'auto':
                return 0
            elif value == 'never':
                return 1
            elif value == 'always':
                return 2
            else:
                return 0
        else:
            return

    def split_behavior_int(self, value):
        # 0 = auto ; 1 = tile ; 2 = overlay ; 3 = displace
        if isinstance(value, int):
            if value < 0 or value > 3:
                return 0
            else:
                return value
        elif isinstance(value, str):
            if value == 'auto':
                return 0
            elif value == 'tile':
                return 1
            elif value == 'overlay':
                return 2
            elif value == 'displace':
                return 3
            else:
                return 0
        else:
            return 0

    def column_int(self, value):
        if isinstance(value, int):
            if value < 0 or value > 3:
                return 0
            else:
                return value
        elif isinstance(value, str):
            if value == 'primary':
                return 0
            elif value == 'supplementary':
                return 1
            elif value == 'secordary':
                return 2
            elif value == 'compact':
                return 3
            else:
                return 0
        else:
            return 0

    @property
    def primary_column_width_fraction(self):
        return self.controller.primaryColumnWidth

    @primary_column_width_fraction.setter
    def primary_column_width_fraction(self, value):
        if value < 0 or value > 1.0:
            print('invalid fraction:', value)
        else:
            self.controller.preferredPrimaryColumnWidthFraction = value

    @property
    def primary_column_width(self):
        return self.controller.primaryColumnWidth

    @primary_column_width.setter
    def primary_column_width(self, value):
        self.controller.preferredPrimaryColumnWidth = value

    @property
    def minimum_primary_column_width(self):
        return self.controller.primaryColumnWidth

    @minimum_primary_column_width.setter
    def minimum_primary_column_width(self, value):
        self.controller.minimumPrimaryColumnWidth = value

    @property
    def maximum_primary_column_width(self):
        return self.controller.primaryColumnWidth

    @maximum_primary_column_width.setter
    def maximum_primary_column_width(self, value):
        self.controller.maximumPrimaryColumnWidth = value

    @property
    def supplementary_column_width_fraction(self):
        return self.controller.supplementaryColumnWidth

    @supplementary_column_width_fraction.setter
    def supplementary_column_width_fraction(self, value):
        if value < 0 or value > 1.0:
            print('invalid fraction:', value)
        else:
            self.controller.preferredSupplementaryColumnWidthFraction = value

    @property
    def supplementary_column_width(self):
        return self.controller.supplementaryColumnWidth

    @supplementary_column_width.setter
    def supplementary_column_width(self, value):
        self.controller.preferredSupplementaryColumnWidth = value

    @property
    def minimum_supplementary_column_width(self):
        return self.controller.supplementaryColumnWidth

    @minimum_supplementary_column_width.setter
    def minimum_supplementary_column_width(self, value):
        self.controller.minimumSupplementaryColumnWidth = value

    @property
    def maximum_supplementary_column_width(self):
        return self.controller.supplementaryColumnWidth

    @maximum_supplementary_column_width.setter
    def maximum_supplementary_column_width(self, value):
        self.controller.maximumSupplementaryColumnWidth = value
