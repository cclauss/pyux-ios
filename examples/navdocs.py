import json
import configparser
import collections

import ux

with open('./uxdocs.json') as in_file:
    uxdocs = json.load(in_file)
    
def loadConfig(file, config={}):
    config = collections.OrderedDict(config.copy())
    cp = configparser.ConfigParser(dict_type=collections.OrderedDict, interpolation=None)
    cp.read(file)
    for sec in cp.sections():
        name = sec.lower()
        for opt in cp.options(sec):
            config[name + "." + opt.lower()] = cp.get(sec, opt).strip()
    return config

htmldef = loadConfig('./uxdocs.ini')

    
HTML = """<html><head>
    <meta charset="utf-8"> 
    <h3>Hello HTML</h3></html>'
"""    

HTML = """<html><head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">

<style>/*---------------------------------------------------
    LESS Elements 0.9
  ---------------------------------------------------
    A set of useful LESS mixins
    More info at: http://lesselements.com
  ---------------------------------------------------*/
/**
 * https://github.com/rhiokim/markdown-css
 * solarized-light style
 * made by rhio.kim
 * powered by http://ethanschoonover.com/solarized
 */
body {
  padding: 20px;
  color: #ffffff;
  font-size: 1em;
  font-family: Sans-serif;
  background: #282a36;
  -webkit-font-smoothing: antialiased;
}
a {
  color: #e03300;
}
a:hover {
  color: #ff4a14;
}
h2 {
  border-bottom: 1px solid #21232d;
}
h6 {
  color: #a4a296;
}
hr {
  border: 1px solid #21232d;
}
pre > code {
/*  font-size: .9em;*/
  font-family: Consolas, Inconsolata, Courier, monospace;
}
blockquote {
  border-left: 4px solid #121319;
  padding: 0 15px;
  font-style: italic;
}
table {
  background-color: #303241;
}
table tr th,
table tr td {
  border: 1px solid #4b4e65;
}
table tr:nth-child(2n) {
  background-color: #373a4b;
}
/**
 * after less
 */
</style>
</head>
<body>
{body}
</body>
</html>
"""
    
class DocViewer(ux.WebView):
  
    def webview_did_finish_load(self, webview):
        print('webview_did_finish_load')
    
class TableView2():
    
    def __init__(self, parent):
        self.parent = parent
        self.tv = ux.TableView()
        self.tv.frame = (0, 0, 580, 620)
        self.tv.flex = 'WH'
        self.tv.delete_enabled = False
        self.tv.move_enabled = False
        self.tv.data_source = self.tv.delegate = self
        self.tv.action = self.table_did_select
        self.webview = DocViewer()
        #self.webview.ensure_vc()
        self.webview.name = 'Details'
        self.webview.flex = 'WH'

    def refresh(self, sender=None):
        print('refresh...')
        self.tv.name = uxdocs['classes'][self.key]['name']
        self.dsitems = []
        cls = uxdocs['classes'][self.key]
        for i, key in enumerate(cls.keys()):
            if isinstance(cls[key], dict):
                rows = []
                for fn in cls[key].keys():
                    subtitle = str(cls[key][fn])
                    style = 'default' if subtitle == '--' else 'subtitle' 
                    rows.append({'title':fn,
                            'subtitle': subtitle,
                            'style': style,
                            'image': None,
                            'accessory_type': 'disclosure_indicator',
                            'html': subtitle
                    })
                self.dsitems.append((key, rows))
            
        self.tv.data = self.dsitems
        self.tv.reload()

    def table_did_select(self, sender):
        print('row %d selected' % self.tv.selected_rows[0][1])
        sec, row = self.tv.selected_rows[0]
        self.webview.frame = self.tv.frame
        self.webview.disable_zoom()
        html = htmldef.get(str(self.tv.name).lower() + '.' + self.tv.data[sec][1][row]['title'], None)
        if html:
            html = html.replace('{tab}', '    ')
            self.webview.load_html(HTML.replace('{body}', html))
        else:
            self.webview.load_html(HTML.replace('{body}', 'error'))
        self.tv.navigation_view.push_view(self.webview)

    def table_accessory_action(self, sender):
        print('accessory row %d selected' % self.tv.selected_rows[0][1])
        
    def tableview_cell_for_row(self, tableview, section, row):
        return self.tv.data[section][1][row]
    
    def tableview_number_of_sections(self, tableview):
        return len(self.tv.data)

    def tableview_title_for_header(self, tableview, section):
        return self.tv.data[section][0]
        
    def tableview_number_of_rows(self, tableview, section):
        return len(self.tv.data[section][1])

class TableView1():
    
    def __init__(self):
        self.tv = ux.TableView()
        self.tv.frame = (0, 0, 580, 620)
        self.tv.flex = 'WH'
        self.tv.name = 'UX Docs'

        self.tv.delete_enabled = True
        self.tv.move_enabled = True
        self.tv.data_source = self.tv.delegate = self
        self.tv.action = self.table_did_select
        self.tv.accessory_action = self.table_accessory_action
        self.tv.search_action = self.search_handler
        self.table2 = TableView2(None)
        self.refresh()
        self.nav = ux.NavigationView(self.tv)
        self.nav.present('sheet', topbar=False, right_close_button=True)

    def search_handler(self, text):
        print('searching... ', text)
        searchstr = str(text).lower()
        dsitems = []
        for item in self.dsitems:
            if searchstr in item['title'].lower():
                dsitems.append(item)
                
        self.tv.data = dsitems
        self.tv.reload()

    def refresh(self, sender=None):
        print('refresh...')
        self.dsitems = []
        classes = uxdocs['classes']
        for i, key in enumerate(classes.keys()):
            self.dsitems.append({'title':classes[key]['name'],
                            'subtitle': classes[key]['constructor'],
                            'style': 'subtitle',
                            'image': None,
                            'accessory_type': 'disclosure_indicator',
                            'key': key
            }) 
        self.tv.data = self.dsitems
        self.tv.reload()

    def table_did_select(self, sender):
        print('row %d selected' % self.tv.selected_rows[0][1])
        section, row = self.tv.selected_row
        _key = self.dsitems[row]['key']
        self.table2.key = self.dsitems[row]['key']
        self.table2.refresh()
        self.nav.push_view(self.table2.tv)

    def table_accessory_action(self, sender):
        print('accessory row %d selected' % self.tv.selected_rows[0][1])


class UxApp():
    
    def __init__(self):
        TableView1()
        
if __name__ == '__main__':
    UxApp()

