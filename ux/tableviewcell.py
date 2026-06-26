from .font import *

from .uikit import (
    UIFont,
    UITableViewCell,
    UITableViewCellEditingStyleDelete,
    UITableViewCellEditingStyleInsert,
    UITableViewCellEditingStyleNone,
    UITableViewCellSeparatorStyleNone,
    UITableViewCellStyleDefault,
    UITableViewCellStyleSubtitle,
    UITableViewCellStyleValue1,
    UITableViewCellStyleValue2
)

class TableViewCell():
    def __init__(self, style='default', **kwargs):
        if style == 'default':
            self.style = UITableViewCellStyleDefault
        elif style == 'subtitle':
            self.style = UITableViewCellStyleSubtitle
        elif style == 'value1':
            self.style = UITableViewCellStyleValue1
        elif style == 'value2':
            self.style = UITableViewCellStyleValue2
        else:
            self.style = UITableViewCellStyleDefault

        self.native = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(self.style, "rowcell")

    @property
    def text_label(self) -> str:
        return self.native.textLabel

    @property
    def detail_text_label(self):
        return self.native.detailTextLabel

    @property
    def image_view(self):
        return self.native.imageView

    @property
    def accessory_type(self) -> str:
        return self.native.accessoryType.text

    @accessory_type.setter
    def accessory_type(self, accessory):
        if accessory == 'disclosure_indicator':
            self.native.accessoryType = 1
        elif accessory == 'detail_disclosure_button':
            self.native.accessoryType = 2
        elif accessory == 'checkmark':
            self.native.accessoryType = 3
        elif accessory == 'detail_button':
            self.native.accessoryType = 4
        else:
            self.native.accessoryType = 0

    @property
    def bounds(self):
        return (self.native.contentView.bounds.origin.x,
                self.native.contentView.bounds.origin.y,
                self.native.contentView.bounds.size.width,
                self.native.contentView.bounds.size.height)
    
    @property
    def content_view(self):
        return self.native.contentView

    def add_subview(self, content):
        self.native.contentView.addSubview(content.native)
