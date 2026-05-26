from .uikit import (UIFont)

class Font():

    def named(font):
        if isinstance(font, tuple):
            if font[0] == '<system>':
                return UIFont.systemFontOfSize(font[1])
            return UIFont.fontWithName(font[0], size=font[1])

        return None

