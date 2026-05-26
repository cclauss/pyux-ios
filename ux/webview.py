#coding: utf-8

"""
adapted from: https://github.com/mikaelho/pythonista-webview
"""

from rubicon.objc import (
    Block, CGRect, CGPoint, CGSize, NSObject, NSPoint, ObjCClass, ObjCInstance, ObjCProtocol, SEL,
    ns_from_py, objc_method, objc_rawmethod, objc_property, py_from_ns, send_message, send_super
)
from rubicon.objc.runtime import get_class, objc_id, add_method
from rubicon.objc.types import UnknownPointer, register_preferred_encoding

import webbrowser
import queue, weakref, ctypes, functools, time, os, json, re, sys
from types import SimpleNamespace
from typing import Callable, Any
from ctypes import c_void_p, c_int, c_ulong, c_char_p, Structure, addressof, CFUNCTYPE, byref, py_object
from .alerts import alert, input_alert
from .core import in_background, on_main_thread
from .view import View

from threading import Thread, current_thread, main_thread

from .foundation import NSURL, NSURLRequest

from .uikit import (
    UIColor,
    WKWebView,
    WKWebViewConfiguration,
    WKWebpagePreferences,
    WKUserContentController,
    WKUserScript,
    WKWebsiteDataStore
)

class _block_descriptor (Structure):
    _fields_ = [
        ('reserved', c_ulong),
        ('size', c_ulong),
        ('copy_helper', c_void_p),
        ('dispose_helper', c_void_p),
        ('signature', c_char_p)
    ]

def _block_literal_fields(*arg_types):
    return [
        ('isa', c_void_p),
        ('flags', c_int),
        ('reserved', c_int),
        ('invoke', ctypes.CFUNCTYPE(c_void_p, c_void_p, *arg_types)),
        ('descriptor', _block_descriptor)
    ]

class struct_handler(Structure):
    pass # No _fields_, because this is an opaque structure.

def get_message_handler():
    if get_class('CustomMessageHandler').value is not None:
        #print('duplicate')
        return ObjCClass(get_class('CustomMessageHandler'))
    else:
        class CustomMessageHandler(NSObject):

            interface = objc_property(object, weak=True)

            @objc_method
            def userContentController_didReceiveScriptMessage_(self, contentController, message) -> None:
                wk_message = ObjCInstance(message)
                name = str(wk_message.name)
                content = str(wk_message.body)
                self.interface.webview_message_received({ 'name': name, 'content': content })
                return None

        return CustomMessageHandler

def get_webview():
    if get_class('uxWebView').value is not None:
        return ObjCClass(get_class('uxWebView'))
    else:
        class uxWebView(WKWebView):
            interface = objc_property(object, weak=True)

            @objc_rawmethod
            def webView_decidePolicyForNavigationAction_decisionHandler_( self, _cmd, webview,
                   _navigation_action, decisionHandler: c_void_p) -> None:
                completion_handler = ObjCInstance(decisionHandler)
                completion_handler.retain()

                ObjCInstance(webview).interface._decision_handler(_navigation_action, decisionHandler)

            @objc_method
            def webView_didCommitNavigation_(self, navigation) -> None:
                self.interface.webview_did_start_load(self.interface)

            @objc_method
            def webView_didFinishNavigation_(self, navigation) -> None:
                self.interface.webview_did_finish_load(self.interface)

            @objc_method
            def webView_didFailProvisionalNavigation_withError_(self, webview, navigation, error) -> None:
                err = ObjCInstance(error)
                error_code = int(err.code)
                error_msg = str(err.localizedDescription)
                print('load failed...', error_code, error_msg)
                self.interface.webview_did_fail_load(self.interface, error_code, error_msg)

            @objc_rawmethod
            def webView_runJavaScriptAlertPanelWithMessage_initiatedByFrame_completionHandler_(
                    self, _cmd, webview, message, frame, completionHandler: c_void_p) -> None:

                completion_handler = ObjCInstance(completionHandler)
                completion_handler.retain()

                ObjCInstance(webview).interface._javascript_alert(message, frame, completionHandler)

            @objc_rawmethod
            def webView_runJavaScriptConfirmPanelWithMessage_initiatedByFrame_completionHandler_(
                    self, _cmd, webview, message, frame, completionHandler: c_void_p) -> None:

                completion_handler = ObjCInstance(completionHandler)
                completion_handler.retain()

                ObjCInstance(webview).interface._javascript_confirm(message, frame, completionHandler)

            @objc_rawmethod
            def webView_runJavaScriptTextInputPanelWithPrompt_defaultText_initiatedByFrame_completionHandler_(
                    self, _cmd, webview, prompt, default_text, frame, completionHandler: c_void_p) -> None:

                completion_handler = ObjCInstance(completionHandler)
                completion_handler.retain()

                ObjCInstance(webview).interface._javascript_prompt(prompt, default_text, frame, completionHandler)

        return uxWebView

class WebView(View):

    def __init__(self,
            delegate=None,
            swipe_navigation=False,
            log_js_evals=False,
            respect_safe_areas=False,
            inline_media=None,
            airplay_media=True,
            pip_media=True,
            allowscript=True,
            **kwargs
        ):
        super().__init__(**kwargs)
        self._delegate = self
        if delegate:
            self.delegate = delegate
        self.allowscript =  allowscript
        self.wkclass = get_webview()
        self.eval_js_queue = queue.Queue()
        if not self.native.backgroundColor:
            self.native.backgroundColor = UIColor.systemBackgroundColor()

        self._create_webview()

    @on_main_thread
    def _create_webview(self):
        webview_config = WKWebViewConfiguration.new()
        self.user_content_controller = webview_config.userContentController
        webview_config.preferences.setValue_forKey_(True,
            'allowFileAccessFromFileURLs')
        webview_config.preferences.setValue_forKey_(self.allowscript,
            'javaScriptEnabled')

        try:
            message_handler = get_message_handler()
            custom_message_handler = message_handler.new()
            custom_message_handler.interface = self
            webview_config.userContentController.addScriptMessageHandler_name_(custom_message_handler, 'jsmessage')
        except:
            print(str(sys.exc_info()))
            print('WKScriptMessageHandler protocol is not available')

        self.webview = self.wkclass.alloc().\
            initWithFrame_configuration_(
            ((0,0), (self.width, self.height)), webview_config)

        self.webview.interface = self
        self.webview.autoresizingMask = 2 + 16 # WH
        self.webview.navigationDelegate = self.webview
        self.webview.UIDelegate = self.webview
        ObjCInstance(self.objc_instance).addSubview_(self.webview)

    def layout(self):
        pass

    @on_main_thread
    def load_url(self, url, no_cache=False, timeout=10):
        """ Loads the contents of the given url
        asynchronously.

        If the url starts with `file://`, loads a local file. If the remaining
        url starts with `/`, path starts from Pythonista root.

        For remote (non-file) requests, there are
        two additional options:

          * Set `no_cache` to `True` to skip the local cache, default is `False`
          * Set `timeout` to a specific timeout value, default is 10 (seconds)
        """

        if url.startswith('file://'):
            file_path = url[7:]
            if file_path.startswith('/'):
                root = os.path.expanduser('~')
                file_path = root + file_path
            else:
                current_working_directory = os.path.dirname(os.getcwd())
                file_path = current_working_directory+'/' + file_path
            dir_only = os.path.dirname(file_path)
            file_path = NSURL.fileURLWithPath_(file_path)
            dir_only = NSURL.fileURLWithPath_(dir_only)
            self.webview.loadFileURL_allowingReadAccessToURL_(
                file_path, dir_only)
        else:
            cache_policy = 1 if no_cache else 0
            self.webview.loadRequest_(
                NSURLRequest.
                    requestWithURL_cachePolicy_timeoutInterval_(
                        NSURL.URLWithString(url),
                        cache_policy,
                        timeout))

    @on_main_thread
    def load_html(self, html):
        # Need to set a base directory to get
        # real js errors
        current_working_directory = os.path.dirname(os.getcwd())
        root_dir = NSURL.fileURLWithPath_(current_working_directory)
        self.webview.loadHTMLString_baseURL_(html, root_dir)

    def eval_js(self, javascript):
        self.eval_js_async(javascript)
        value = self.eval_js_queue.get()
        return value

    @on_main_thread
    def eval_js_async(self, javascript, on_result=None):

        @Block
        def js_handler(res: objc_id, error: objc_id) -> None:
            self.eval_js_queue.put(py_from_ns(res))

        self.webview.evaluateJavaScript(
            javascript,
            completionHandler=js_handler
        )

    @property
    def delegate(self):
        return (self._delegate)

    @delegate.setter
    def delegate(self, cls):
        self._delegate = cls

        if hasattr(cls, 'webview_should_start_load'):
            self.webview_should_start_load = cls.webview_should_start_load

        if hasattr(cls, 'webview_did_start_load'):
            self.webview_did_start_load = cls.webview_did_start_load

        if hasattr(cls, 'webview_did_finish_load'):
            self.webview_did_finish_load = cls.webview_did_finish_load

        if hasattr(cls, 'webview_did_fail_load'):
            self.webview_did_fail_load = cls.webview_did_fail_load

        if hasattr(cls, 'webview_message_received'):
            self.webview_message_received = cls.webview_message_received

    @on_main_thread
    def go_back(self):
        self.webview.goBack()

    @on_main_thread
    def go_forward(self):
        self.webview.goForward()

    @on_main_thread
    def reload(self):
        self.webview.reload()

    @on_main_thread
    def stop(self):
        self.webview.stopLoading()

    def add_script(self, js_script, add_to_end=True):
        location = 1 if add_to_end else 0
        wk_script = WKUserScript.alloc().\
            initWithSource_injectionTime_forMainFrameOnly_(
                js_script, location, False)

        self.user_content_controller.addUserScript_(wk_script)

    def add_style(self, css):
        """
        Convenience method to add a style tag with the given css, to every
        page loaded by the view.
        """
        css = css.replace("'", "\'")
        js = f"""var style = document.createElement('style');
        style.innerHTML = '{css}';"
        document.getElementsByTagName('head')[0].appendChild(style);"""
        self.add_script(js, add_to_end=True)

    def add_meta(self, name, content):
        """
        Convenience method to add a meta tag with the given name and content,
        to every page loaded by the view."
        """
        name = name.replace("'", "\'")
        content = content.replace("'", "\'")
        js = f"""var meta = document.createElement('meta');
        meta.setAttribute('name', '{name}');
        meta.setAttribute('content', '{content}');
        document.getElementsByTagName('head')[0].appendChild(meta);"""
        self.add_script(js, add_to_end=True)

    def disable_zoom(self):
        name = 'viewport'
        content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
        self.add_meta(name, content)

    def disable_user_selection(self):
        css = '* { -webkit-user-select: none; }'
        self.add_style(css)

    def disable_font_resizing(self):
        css = 'body { -webkit-text-size-adjust: none; }'
        self.add_style(css)

    def disable_scrolling(self):
        """
        Included for consistency with the other `disable_x` methods, this is
        equivalent to setting `scroll_enabled` to false."
        """
        self.scroll_enabled = False

    def disable_all(self):
        """
        Convenience method that calls all the `disable_x` methods to make the
        loaded pages act more like an app."
        """
        self.disable_zoom()
        self.disable_scrolling()
        self.disable_user_selection()
        self.disable_font_resizing()

    def _decision_handler(self, navigation_action, decisionHandler):

        class _block_decision_handler(Structure):
            _fields_ = _block_literal_fields(ctypes.c_long)

        def _callback(rs):
            blk = _block_decision_handler.from_address(
                decisionHandler)

            if rs:
                blk.invoke(decisionHandler, True)
            else:
                blk.invoke(decisionHandler, False)

        nav_action = ObjCInstance(navigation_action)
        ns_url = nav_action.request.URL
        url = str(ns_url)
        nav_type = int(nav_action.navigationType)

        allow = self.webview_should_start_load(self, url, nav_type)
        _callback(allow)

    def _javascript_alert(self, _message, _frame, completionHandler):

        class _block_alert_completion(Structure):
            _fields_ = _block_literal_fields()

        def _callback(rs):
            blk = _block_alert_completion.from_address(
                completionHandler)

            blk.invoke(completionHandler)

        message = str(ObjCInstance(_message))
        host = str(ObjCInstance(_frame).request.URL.host)

        if host == 'None': host = 'Local'
        alert(host, message, 'Ok', hide_cancel_button=True, callback=_callback)

    def _javascript_confirm(self, _message, _frame, completionHandler):

        class _block_confirm_completion(Structure):
            _fields_ = _block_literal_fields(ctypes.c_bool)

        def _callback(rs):
            blk = _block_confirm_completion.from_address(
                completionHandler)

            if rs:
                blk.invoke(completionHandler, True)
            else:
                blk.invoke(completionHandler, False)

        message = str(ObjCInstance(_message))
        host = str(ObjCInstance(_frame).request.URL.host)

        if host == 'None': host = 'Local'
        alert(host, message, 'Ok', callback=_callback)

    def _javascript_prompt(self, _prompt, _text, _frame, completionHandler):

        class _block_text_completion(Structure):
            _fields_ = _block_literal_fields(c_void_p)

        def _callback(rs):
            blk = _block_text_completion.from_address(
                completionHandler)

            if rs:
                blk.invoke(completionHandler, ns_from_py(rs))
            else:
                blk.invoke(completionHandler, ns_from_py(rs))

        prompt = str(ObjCInstance(_prompt))
        txt = str(ObjCInstance(_text))
        host = str(ObjCInstance(_frame).request.URL.host)
        if host == 'None': host = 'Local'
        input_alert(prompt, txt, callback=_callback)

    def webview_should_start_load(self, webview, url, nav_type):
        return True

    def webview_did_start_load(self, webview):
        #print('webview_did_start_load')
        pass

    def webview_did_finish_load(self, webview):
        #print('webview_did_finish_load')
        pass

    def webview_did_fail_load(self, webview, error_code, error_msg):
        #print(error_code, error_msg)
        pass

    def webview_message_received(self, message):
        #print('message recieved')
        pass
