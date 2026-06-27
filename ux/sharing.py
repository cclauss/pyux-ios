from rubicon.objc import ObjCClass
from .core import asyncq, topvc

from .foundation import NSURL


NSItemProvider = ObjCClass("NSItemProvider")
UIActivityItemsConfiguration = ObjCClass("UIActivityItemsConfiguration")
UIActivityViewController = ObjCClass("UIActivityViewController")

class ShareSheet():
    def __init__(self, type='text', data=None, result=None, callback=None):

        self.native = None
        if data:
            if type == 'text':
                text = data.encode()
                provider = NSItemProvider.new().initWithItem(text, typeIdentifier='public.plain-text')
                config = UIActivityItemsConfiguration.new().initWithItemProviders([provider])
                self.native = UIActivityViewController.alloc().initWithActivityItemsConfiguration(config)
            elif type == 'url':
                nsurl = NSURL.URLWithString(str(data))
                self.native = UIActivityViewController.alloc().initWithActivityItems([nsurl], applicationActivities=None)
            elif isinstance(data, list):
                self.native = UIActivityViewController.alloc().initWithActivityItems(data, applicationActivities=None)
            else:
                self.native = UIActivityViewController.alloc().initWithActivityItems([data], applicationActivities=None)

    def present(self):
        top = topvc()

        def _present(_self):
            top.presentViewController_animated_completion_(self.native, True, None)

        if self.native:
            asyncq(_present)

