import os
from .core import media_path
from .uikit import (UIImage)

class Image():

    def named(name):

        if name[:7] == 'system:':
            return UIImage.systemImageNamed_(name.split(':')[1])
        if ':' in name:
            ipath = os.path.join(media_path, 'Images/' + name.replace(':', '/'))

            if os.path.exists(str(ipath)) or os.path.exists(str(ipath) + '.png'):
                return UIImage.alloc().initWithContentsOfFile_(str(ipath))
        else:
            if os.path.exists(str(name)) or os.path.exists(str(name) + '.png'):
                return UIImage.alloc().initWithContentsOfFile_(str(name))

        return None
