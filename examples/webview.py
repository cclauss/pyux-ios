#!python3

import ux

HTML = """<html><head>
    <meta charset="utf-8"> 
    <h3>Hello HTML</h3></html>'
"""
# <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0, user-scalable = no">

class WebViewDemo(ux.View):
    def __init__(self, url, flex='WH'):
        ux.View.__init__(self)
        self.webview = ux.WebView(delegate=self, flex='WH')
        self.add_subview(self.webview)

        menuitems = [
            ('Home', self.actions),
            ('Html', self.actions),
            ('Python.org', self.actions)
        ]
        menu = ux.Menu('Actions', menuitems)
        self.right_button_items = [
            ux.ButtonItem(image=ux.Image.named('system:x.circle'), action=self.nav_stop),
            ux.ButtonItem(image=ux.Image.named('system:gobackward'), action=self.nav_reload),
            ux.ButtonItem(image=ux.Image.named('system:chevron.right'), action=self.nav_fwd),
            ux.ButtonItem(image=ux.Image.named('system:chevron.left'), action=self.nav_back),
            ux.ButtonItem(image=ux.Image.named('system:bookmark'), action=None, menu=menu)
        ]

        self.webview.load_url(url)
        
    def webview_should_start_load(self, webview, url, nav_type):
        if url.startswith('file://'):
            return True
        else:
            #return False # restrict url 
            return True    
    
    def webview_did_start_load(self, webview):
        print('-start loading-')
                
    def webview_did_finish_load(self, webview):
        print('-finish loading-')

    def webview_did_fail_load(self, webview, error_code, error_msg):
        print(error_msg)

    @ux.in_background
    def webview_message_received(self, message):
        print('Message received: ' + message['content'])
        sendstr = "alert('Python received your message: " + message['content'] + "');"
        self.webview.eval_js(sendstr) 
    
    def actions(self, sender, args=None):
        action = sender.Header if sys.platform == 'win32' else sender.title
        print('action', action)
        if action == 'Home':
            url = 'file://webapps/www/testit.htm'
            self.webview.load_url(url)
            
        elif action == 'Html':
            print(HTML)
            self.webview.disable_zoom()
            self.webview.load_html(HTML)
        
        elif action == 'Python.org':
            self.webview.load_url('https://python.org', no_cache=True)
            
    def nav_back(self, sender):
        print('go back')
        self.webview.go_back()
        
    def nav_fwd(self, sender):
        print('go forward')
        self.webview.go_forward()
        
    def nav_reload(self, sender):
        print('reload')
        self.webview.reload()
        
    def nav_stop(self, sender):
        print('stop')
        self.webview.stop()
        
        
if __name__ == '__main__':
    #url = 'http://192.168.1.80/examples/webview.htm'
    #url = 'file:///Documents/examples/webview.htm'
    url = 'file://examples/webview.htm'
    w = WebViewDemo(url)
    w.present()