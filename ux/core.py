import sys
import os
import time
from collections import namedtuple
from rubicon.objc import Block, CGRect, CGPoint, CGSize, ObjCClass, ObjCInstance
from rubicon.objc.runtime import libobjc, objc_block, objc_id, load_library
from rubicon.objc.types import NSTimeInterval
from ctypes import Structure, byref, cast
from threading import Thread, current_thread, Semaphore
#print(__version__)

from .uikit import (
    UIApplication,
    UIDevice,
    UIScreen,
    UIView,
    UIUserInterfaceIdiom,
    UIUserInterfaceStyle,
    UIUserInterfaceSizeClass
)

uxviews = []
uxthread = current_thread().name

uxobjects = { 'nextvar': 0 }

options = {
    'debuglevel': 0,
    'toga': False
}

libSystem = load_library("System")
libdispatch = libSystem

class struct_dispatch_queue_s(Structure):
    pass # No _fields_, because this is an opaque structure.

_dispatch_main_q = struct_dispatch_queue_s.in_dll(libdispatch, "_dispatch_main_q")

def dispatch_get_main_queue():
    return ObjCInstance(cast(byref(_dispatch_main_q), objc_id))

libobjc.dispatch_async.restype = None
libobjc.dispatch_async.argtypes = [
  objc_id,
  objc_block,
]

def block_code(_self):
    dprint("async_q!!")

def asyncq(fn):
    dprint('fn')
    global blockq
    blockq = Block(fn, None, (objc_id))
    libobjc.dispatch_async(dispatch_get_main_queue(), blockq)

global blockq

def dprint(*args):
    if options['debuglevel'] > 0:
        print('debug: ', args)

py3kit = True if 'Pythonista3.app' in sys.executable else False
pyto = True if 'Pyto.app' in sys.executable else False

if py3kit:
    media_path = os.path.join(os.path.dirname(sys.executable), 'Media')
else:
    media_path = os.path.join(os.path.dirname(__file__), 'media')

def ios_version() -> str:
    return str(UIDevice.currentDevice.systemVersion)

def ios_version_info():
    iOSVersion = namedtuple("ios_version_info", "major minor micro")
    vlist = [int(p) for p in str(UIDevice.currentDevice.systemVersion).split(".")]
    if len(vlist) == 2:
        vlist.append(0)
    return iOSVersion(vlist[0], vlist[1], vlist[2])

apppath = os.path.dirname(sys.executable)

def get_screen_size():
    screenRect = UIScreen.mainScreen.bounds
    screenWidth = screenRect.size.width
    screenHeight = screenRect.size.height
    return (screenWidth, screenHeight)

def get_window_size():
    window = UIApplication.sharedApplication.keyWindow
    winRect = window.bounds
    winWidth = winRect.size.width
    winHeight = winRect.size.height
    return (winWidth, winHeight)

def get_window_traits():
    obj = UIScreen.mainScreen.traitCollection
    dprint(UIUserInterfaceStyle.dark.value)
    return { 'idiom': UIUserInterfaceIdiom(obj.userInterfaceIdiom).name,
             'style': UIUserInterfaceStyle(obj.userInterfaceStyle).name,
             'hsize_class': UIUserInterfaceSizeClass(obj.horizontalSizeClass).name,
             'vsize_class': UIUserInterfaceSizeClass(obj.verticalSizeClass).name,
           }

def rootvc():
    root = UIApplication.sharedApplication.keyWindow.rootViewController
    dprint(root)
    return root

def topvc():
    top = UIApplication.sharedApplication.keyWindow.rootViewController
    while True:
        if top.presentedViewController:
            top = top.presentedViewController
        elif top.isKindOfClass(ObjCClass('UINavigationController')):
            top = top.visibleViewController
        elif top.isKindOfClass(ObjCClass('UITabBarController')):
            top = top.selectedViewController
        else:
            break

    if top.isBeingDismissed():
        top = top.presentingViewController
    dprint('core', current_thread().name)
    dprint(top)
    return top

def _in_background(fn, *args, **kwargs):
    dprint('_in_background', current_thread().name)
    d1 = Thread(target=fn, args=args)
    d1.start()

def in_background(fn):
    def run(*args, **kwargs):
        def _run():
            return fn(*args, **kwargs)

        if current_thread().name.startswith('Main') and options['toga']:
            return _in_background(_run)
        elif current_thread().name.startswith('Dummy'):
            return _in_background(_run)
        else:
            return(fn(*args, **kwargs))

    return run

def on_main_thread(fn):
    def run(*args, **kwargs):

        def _run(_self):
            return fn(*args, **kwargs)

        if not current_thread().name.startswith('Main') and options['toga']:
            return asyncq(_run)
        elif not current_thread().name.startswith('Dummy'):
            return asyncq(_run)
        else:
            return(fn(*args, **kwargs))

    return run

def convert_point(point=(0, 0), from_view=None, to_view=None):
    if isinstance(point, tuple):
        px, py = point
        nspoint = CGPoint(px, py)
    else:
        nspoint = CGPoint(0, 0)

    window = UIApplication.sharedApplication.keyWindow
    if from_view and to_view:
        newpoint = from_view.native.convertPoint(nspoint, toView=to_view.native)
        return (newpoint.x, newpoint.y)
    elif from_view:
        newpoint = window.convertPoint(nspoint, fromView=from_view.native)
        return (newpoint.x, newpoint.y)
    elif to_view:
        newpoint = window.convertPoint(nspoint, toView=to_view.native)
        return (newpoint.x, newpoint.y)

def convert_rect(rect=(0, 0, 0, 0), from_view=None, to_view=None):
    if isinstance(rect, tuple):
        rx, ry, rw, rh = rect
        nsrect = CGRect(CGPoint(rx, ry), CGSize(rw, rh))
    else:
        nsrect = CGRect(CGPoint(0, 0), CGSize(0, 0))

    window = UIApplication.sharedApplication.keyWindow
    if from_view and to_view:
        newrect = from_view.native.convertRect(nsrect, toView=to_view.native)
        return (newrect.origin.x,
            newrect.origin.y,
            newrect.size.width,
            newrect.size.height)
    elif from_view:
        newrect = window.convertRect(nsrect, fromView=from_view.native)
        return (newrect.origin.x,
            newrect.origin.y,
            newrect.size.width,
            newrect.size.height)
    elif to_view:
        newrect = window.convertRect(nsrect, toView=to_view.native)
        return (newrect.origin.x,
            newrect.origin.y,
            newrect.size.width,
            newrect.size.height)

def animate(fn, duration):
    def _animate(x):
        def _fn(_cmd):
            fn()

        fnblock = Block(_fn, None, objc_id)
        UIView.animateWithDuration(NSTimeInterval(duration), animations=fnblock)

    asyncq(_animate)

def will_block(callback):
    block_message = """
    this will block
    use callback
    """
    if callback is None and not current_thread().name.startswith('Thread'):
        print(block_message)
        return True

    return False

class waitModal():
    def __init__(self):
        self.done = False
        self.result = None
        self.semaphore = Semaphore(0)

    def wait(self, interval=0.3, duration=3):
        waitcount = 0
        for n in range(int(duration/interval)):
            try:
                time.sleep(interval)
                dprint('wait -|-', n)
                if self.done:
                    break
                waitcount += 1
                if waitcount == 100:
                    self.done = [-1, 'none', 'none']
                    break
            except:
                dprint("Exception ",str(sys.exc_info()))
                break
        if not self.done:
            self.semaphore.acquire()

    def set_result(self, value, done=True):
        self.result = value
        if done:
            self.set_done()

    def set_done(self):
        self.done = True
        self.semaphore.release()
