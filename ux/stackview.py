from enum import Enum

from .uikit import NSLayoutConstraint, UILayoutConstraintAxis, UIStackView
from .viewcore import ViewCore


class UIStackViewAlignment(Enum):
    Fill = 0
    Leading = 1
    Top = 1
    FirstBaseline = 2
    Center = 3
    Trailing = 4
    Bottom = 4
    LastBaseline = 5

class UIStackViewDistribution(Enum):
    Fill = 0
    FillEqually = 1
    FillProportionally = 2
    EqualSpacing = 3
    EqualCentering = 4

class StackView(ViewCore):
    def __init__(self, **kwargs):
        self.init()
        self.native = UIStackView.alloc().init()
        for arg in kwargs:
            if arg == 'alignment':
                self.alignment = kwargs[arg]
            elif arg == 'axis':
                self.axis = kwargs[arg]
            elif arg == 'distribution':
                self.distribution = kwargs[arg]
            elif arg == 'spacing':
                self.spacing = kwargs[arg]
            else:
                if not self.viewattrs(arg, kwargs[arg]):
                    print('invalid stackview argument: ' + arg)

    @property
    def alignment(self):
        return  self.native.alignment

    @alignment.setter
    def alignment(self, value):
        if isinstance(value, int):
            if value < 0 or value > 5:
                print('align', 0)
            else:
                print('align', value)

        elif value == 'fill':
            self.native.alignment = UIStackViewAlignment.Fill.value
        elif value == 'leading':
            self.native.alignment = UIStackViewAlignment.Leading.value
        elif value == 'top':
            self.native.alignment = UIStackViewAlignment.Top.value
        elif value == 'first_baseline':
            self.native.alignment = UIStackViewAlignment.FirstBaseline.value
        elif value == 'center':
            self.native.alignment = UIStackViewAlignment.Center.value
        elif value == 'trailing':
            self.native.alignment = UIStackViewAlignment.Trailing.value
        elif value == 'bottom':
            self.native.alignment = UIStackViewAlignment.Bottom.value
        elif value == 'last_baseline':
            self.native.alignment = UIStackViewAlignment.LastBaseline.value
        else:
            print('Invalid UIStackViewAlignment', value)

    @property
    def axis(self):
        return self.native.axis

    @axis.setter
    def axis(self, value):
        if value == 'horizontal':
            self.native.axis = UILayoutConstraintAxis.Horizontal.value
        else:
            self.native.axis = UILayoutConstraintAxis.Vertical.value

    @property
    def distribution(self) -> str:
        return self.native.distribution

    @distribution.setter
    def distribution(self, value):
        if isinstance(value, int):
            if value < 0 or value > 4:
                self.native.distribution = 0
            else:
                self.native.distribution = value
        elif value == 'fill':
            self.native.distribution = UIStackViewDistribution.Fill.value
        elif value == 'fill_equally':
            self.native.distribution = UIStackViewDistribution.FillEqually.value
        elif value == 'fill_proportionally':
            self.native.distribution = UIStackViewDistribution.FillProportionally.value
        elif value == 'equally_spacing':
            self.native.distribution = UIStackViewDistribution.EqualSpacing.value
        elif value == 'equal_centering':
            self.native.distribution =  UIStackViewDistribution.EqualCentering.value
        else:
            print('Invalid UIStackViewDistribution', value)

    @property
    def spacing(self):
        return self.native.spacing

    @spacing.setter
    def spacing(self, value):
        if value:
            self.native.spacing = value

    def add_subview(self, content):
        self.native.addArrangedSubview(content.native)
        if self.native.axis == 0:
            if self.distribution == 0 and content.width > 0:
                NSLayoutConstraint.activateConstraints_([
                    content.native.widthAnchor.constraintEqualToConstant_(content.width)
                ])
        else:
            if self.distribution == 0 and content.height > 0:
                NSLayoutConstraint.activateConstraints_([
                    content.native.heightAnchor.constraintEqualToConstant_(content.height)
                ])
