ux.dialogs
==========

Using the callback option with alerts and dialogs is highly recommended.
Modal alerts and dialogs without the callback option need to be called
 from a function using the @ux.in_background decorator.

```
import ux
from ux.dialogs import dialogs  #separate import required

@ux.in_background
def text_modal(sender):

    result = dialogs.text_dialog(title='Text Dialog', text=textstr)
    print(result)

def text_callback(sender):

    def _callback(result):
        print(result)

    dialogs.text_dialog(title='Text Dialog', text='This is a callback dialog', callback=_callback)

```

dialogs.**date_dialog**(title='', style='inline', callback=None)

- style:
  - 0 or 'auto'
  - 1 or 'wheels'
  - 2 or 'compact'
  - 3 or 'inline'
- Cancel returns None
- Optional callback sends result to callable

dialogs.**datetime_dialog**(title='', style='inline', callback=None)

- style:
  - 0 or 'auto'
  - 1 or 'wheels'
  - 2 or 'compact'
  - 3 or 'inline'
- Cancel returns None
- Optional callback sends result to callable

dialogs.**pick_document**(types=['public.item'], return_native=False, callback=None)

- types - List of Universal Type Identifiers (UTIs)
- return_native - return native urls
- Optional callback sends result to callable
- returns urls to temporary files that need to to copied

dialogs.**list_dialog**(title='', items=None, callback=None)

```
# items can be list of strings
items = ['Add', 'Edit', 'Delete']
result = dialogs.list_dialog(title='List Dialog', items=items)

# or sequence of [id, name, accessory_type]
items = [[1, 'Add', 'none'], [2, 'Edit', 'checkmark'], [3, 'Delete', 'none']]
result = dialogs.list_dialog(title='List Dialog', items=items)
```
- Cancel returns None
- Optional callback sends result to callable

dialogs.**form_dialog**(title='', fields=None, sections=None, listdone=None, callback=None)

```
accounts = [[1, 'Checking', 'none'], [2, 'Savings', 'none'], [3, 'Cash', 'none']]

today = date.today()
fields = [
    {'key': 'expenseid', 'title': 'expenseid', 'type': 'int', 'hidden': True, 'value': '0'},
    {'key': 'oper', 'title': 'oper', 'type': 'text', 'hidden': True, 'value':'add'},
    {'key': 'cleared', 'title': 'Cleared', 'type': 'switch', 'value': True},
    {'key': 'payee', 'title': 'Payee', 'type': 'text', 'value':'Cateye Cafe'},
    {'key': 'account', 'title': 'Account', 'type': 'list', 'items': accounts, 'id': 3, 'value': 'Cash'},
    {'key': 'date', 'title': 'Date', 'type': 'date', 'valuex': '2019-12-09','value': today, 'format': '%m/%d/%Y'},
    {'key': 'amount', 'title': 'Amount', 'type': 'decimal', 'value': 3.21},
    {'key': 'note', 'title': 'Note', 'type': 'textview', 'value':'ok'}
]

dialogs.form_dialog(title='Form Dialog', fields=fields, callback=_callback)
```
- fields - List of field dictionaries
- sections - List tuples containing title and field dictionaries [('section 1', fields1), ('section 2', fields2)]
- Use fields or sections, but not both.
- field dictionary keys:
  - key - Key name to use in returned dictionary
  - title - Display title in form
  - type:
  	- check
  	- date
  	- datetime
  	- decimal
  	- email
  	- int
  	- list
  	- number
    - password
  	- switch
  	- text
  	- textview
  	- time
  	- url
  - hidden - boolean
  - value - initial value in form
  - items - Only used when type is 'list'
  - id - Only used when type is 'list' and items are a sequence of [id, name, accessory_type].
  	- The form will display the name column, but return the id column integer.
  - format - Display format option '%m/%d/%Y' for date, datetime and time types.
- Initial value for type 'date' can be a python date object or a formatted string like '2026-06-12'.

dialogs.**share_image**(image)

- share image

dialogs.**share_text**(text)

- share text

dialogs.**share_url**(url)

- share url

dialogs.**share_items**(items=[])

- share items

dialogs.**text_dialog**(title='', text='', callback=None)

- ux.TextView dialog
- Cancel returns None
- Optional callback sends result to callable

dialogs.**time_dialog**(title='', style='wheels')

- style:
  - 0 or 'auto'
  - 1 or 'wheels'
  - 2 or 'compact'
  - 3 or 'inline'
- Cancel returns None
- Optional callback sends result to callable
