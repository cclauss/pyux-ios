from ctypes import c_void_p, cdll

from rubicon.objc import ObjCClass, ObjCInstance, objc_method, py_from_ns
from rubicon.objc.runtime import get_class

from .core import asyncq, options, topvc
from .uikit import UIDocumentPickerViewController

c = cdll.LoadLibrary(None)

def _symbol_ptr(name):
    return c_void_p.in_dll(c, name)

def _str_symbol(name):
    return ObjCInstance(c_void_p.in_dll(c, name))

UTTypeText = _str_symbol('UTTypeItem')

dttypes = {
    'public.item': 'UTTypeItem',
    'public.folder': 'UTTypeFolder',
    'public.content': 'UTTypeContent',
    'public.text': 'UTTypeText'

}

def get_filepicker():
    if get_class('uxFilePicker').value is not None:
        return ObjCClass(get_class('uxFilePicker'))
    else:
        class uxFilePicker(UIDocumentPickerViewController):
            @objc_method
            def documentPicker_didPickDocumentsAtURLs_(self, docpicker, urls) -> None:
                self.interface.nsurls = urls

                if self.interface.action:
                    self.interface.action(py_from_ns(urls))

            @objc_method
            def documentPickerWasCancelled_(self) -> None:
                if self.interface.action:
                    self.interface.action(None)


        return uxFilePicker

class FilePicker():
    def __init__(self, types=['public.item'], result=None, return_native=False, callback=None):
        picktypes = self.types(types)
        self.resultfn = result
        self.return_native = return_native
        self.callback = callback
        filepickclass = get_filepicker()
        if types[0] == 'public.folder':
            self.native = filepickclass.alloc().initForOpeningContentTypes(picktypes, asCopy=False)
        else:
            self.native = filepickclass.alloc().initForOpeningContentTypes(picktypes, asCopy=True)
        #self.native = filepickclass.alloc().initForOpeningContentTypes_asCopy_(picktypes, True)
        self.native.allowsMultipleSelection = True
        self.native.delegate = self.native
        self.native.interface = self
        self.nsurls = None

    def present(self):
        top = topvc()

        def _present(_self):
            top.presentViewController_animated_completion_(self.native, True, None)

        asyncq(_present)

    def types(self, types):

        typelist = []
        for dttype in types:
            typestr = dttypes.get(dttype, None)
            if typestr:
                typelist.append(_str_symbol(typestr))

        return typelist


    def action(self, results):
        if results:
            if self.return_native:
                urls = self.nsurls
            else:
                urls = []
                for url in results:
                    urls.append(str(url.path))

            options['nsurls'] = self.nsurls
        else:
            urls = None
            options['nsurls'] = None

        self.resultfn(urls)
        if self.callback:
            self.callback(urls)
