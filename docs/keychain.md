ux.keychain
===========

```
import ux.keychain as keychain

keychain.set_password('pyux', 'demo1', 'secret1')
keytext1 = keychain.get_password('pyux', 'demo1')
```

Methods
-------

keychain.**new_context**()

- Create new LAContext instance - Local Authentication.

keychain.**get_password**(service, account, context=None)

- Get password for service/account.
- Context option will allow fetching multiple protected values with one authentication. The context is valid for 10 seconds.

keychain.**set_password**(service, account, authentication=None)

- Set password for service/account.
- authentication
  - 'biometric'
  - 'any' - fallback to PIN
  - None

>>   FaceID only available if NSFaceIDUsageDescription key is found in application Info.plist file.
 Pythonista = True  
 Pyto = False


keychain.**delete_password**(service, account)

- Delete password for service/account.

keychain.**get_services**()

- Return a list of all services and accounts that are stored in the keychain (each item is a 2-tuple).
