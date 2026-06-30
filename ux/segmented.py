from rubicon.objc import SEL, ObjCClass, ns_from_py, objc_method, py_from_ns
from rubicon.objc.runtime import get_class

from .colors import uicolor, uicolor_rgba
from .core import get_window_size
from .font import Font
from .uikit import (
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    UIControlEventValueChanged,
    UIControlStateNormal,
    UISegmentedControl,
)
from .viewcore import ViewCore


def get_segcontrol():
    if get_class('uxSegmentedControl').value is not None:
        return ObjCClass(get_class('uxSegmentedControl'))
    else:
        class uxSegmentedControl(UISegmentedControl):
            @objc_method
            def onPress_(self, obj) -> None:
                if self.interface.action:
                    self.interface.action(obj.interface)
        return uxSegmentedControl

class SegmentedControl(ViewCore):
    def __init__(self, **kwargs):
        segclass = get_segcontrol()
        self.native = segclass.alloc().initWithItems_([])
        self.native.interface = self
        self.textAttributes = {}
        self.native.addTarget(self.native, action=SEL('onPress:'), forControlEvents=UIControlEventValueChanged)
        for arg in kwargs:
            if arg == 'enabled':
                self.enabled = kwargs[arg]
            elif arg == 'font':
                self.font = kwargs[arg]
            elif arg == 'highlight_color':
                self.highlight_color = kwargs[arg]
            elif arg == 'segments':
                self.segments = kwargs[arg]
            elif arg == 'selected_index':
                self.selected_index = kwargs[arg]
            elif arg == 'tint_color':
                self.tint_color = kwargs[arg]
            elif arg == 'test':
                self.test()
            else:
                self.viewattrs(arg, kwargs[arg])

    def test(self):
        w, h = get_window_size()
        self.frame = ((w - 220)/2, 50, 220, 40)
        self.segments = ['One', 'Two', 'Three']
        self.selected_index = 0
        self.background_color = 'black'
        self.font = ('Menlo', 18)
        self.tint_color = 'yellow'
        self.highlight_color = 'blue'

    def action(self, sender):
        pass

    @property
    def enabled(self) -> bool:
        return self.native.isUserInteractionEnabled()

    @enabled.setter
    def enabled(self, enable):
        if isinstance(enable, bool):
            self.native.userInteractionEnabled = enable

    @property
    def segments(self):
        items = []
        for idx in range(self.native.numberOfSegments):
            items.append(str(self.native.titleForSegmentAtIndex(idx)))
        return items

    @segments.setter
    def segments(self, segments):
        self.native.removeAllSegments()
        for idx, item in enumerate(segments):
            self.native.insertSegmentWithTitle(item, atIndex=idx, animated=False)

    @property
    def selected_index(self) -> int:
        return self.native.selectedSegmentIndex

    @selected_index.setter
    def selected_index(self, idx):
        if idx in range(self.native.numberOfSegments):
            self.native.selectedSegmentIndex = idx

    @property
    def font(self):
        return (py_from_ns(self.native.font.fontName), py_from_ns(self.native.font.pointSize))

    @font.setter
    def font(self, font):
        self.textAttributes[str(NSFontAttributeName)] = Font.named(font)
        segmentFont = ns_from_py(self.textAttributes)
        self.native.setTitleTextAttributes(segmentFont, forState=UIControlStateNormal)

    @property
    def tint_color(self):
        color = self.textAttributes[str(NSForegroundColorAttributeName)]
        return uicolor_rgba(color)

    @tint_color.setter
    def tint_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.textAttributes[str(NSForegroundColorAttributeName)] = ncolor
            segmentFont = ns_from_py(self.textAttributes)
            self.native.setTitleTextAttributes(segmentFont, forState=UIControlStateNormal)

    @property
    def highlight_color(self):
        color = self.native.selectedSegmentTintColor
        return uicolor_rgba(color)

    @highlight_color.setter
    def highlight_color(self, color):
        ncolor = uicolor(color)
        if ncolor:
            self.native.selectedSegmentTintColor = ncolor
