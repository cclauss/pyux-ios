#!python3

"""
adapted from: https://gist.github.com/zrzka/d1da1dccd626643526747407a0e35135
"""

import os
import plistlib
import sys
from ctypes import POINTER, byref, c_int, c_ulong, c_void_p, cdll
from enum import Enum, IntFlag

from rubicon.objc import ObjCClass, ObjCInstance, ns_from_py, py_from_ns
from rubicon.objc.api import NSArray, NSDictionary
from rubicon.objc.runtime import load_library

load_library('Foundation')
c = cdll.LoadLibrary(None)

NSBundle = ObjCClass('NSBundle')
LocalAuthentication = NSBundle.bundleWithPath_('/System/Library/Frameworks/LocalAuthentication.framework')
LocalAuthentication.load()
LAContext = ObjCClass('LAContext')
NSDate = ObjCClass('NSDate')

def _symbol_ptr(name):
    return c_void_p.in_dll(c, name)

def _str_symbol(name):
    strname = str(ObjCInstance(c_void_p.in_dll(c, name)))
    return strname

# https://developer.apple.com/documentation/security/keychain_services/keychain_items/item_class_keys_and_values?language=objc
kSecClass = _str_symbol('kSecClass')
kSecClassGenericPassword = _str_symbol('kSecClassGenericPassword')
kSecClassInternetPassword = _str_symbol('kSecClassInternetPassword')

# https://developer.apple.com/documentation/security/keychain_services/keychain_items/item_attribute_keys_and_values
# General Item Attribute Keys
kSecAttrAccessControl = _str_symbol('kSecAttrAccessControl')
kSecAttrAccessible = _str_symbol('kSecAttrAccessible')
kSecAttrAccessGroup = _str_symbol('kSecAttrAccessGroup')
kSecAttrSynchronizable = _str_symbol('kSecAttrSynchronizable')
kSecAttrCreationDate = _str_symbol('kSecAttrCreationDate')
kSecAttrModificationDate = _str_symbol('kSecAttrModificationDate')
kSecAttrDescription = _str_symbol('kSecAttrDescription')
kSecAttrComment = _str_symbol('kSecAttrComment')
kSecAttrCreator = _str_symbol('kSecAttrCreator')
kSecAttrType = _str_symbol('kSecAttrType')
kSecAttrLabel = _str_symbol('kSecAttrLabel')
kSecAttrIsInvisible = _str_symbol('kSecAttrIsInvisible')
kSecAttrIsNegative = _str_symbol('kSecAttrIsNegative')
kSecAttrSyncViewHint = _str_symbol('kSecAttrSyncViewHint')

# Password Attribute Keys (generic & internet password)
kSecAttrAccount = _str_symbol('kSecAttrAccount')

# Password Attribute Keys (generic password only)
kSecAttrService = _str_symbol('kSecAttrService')
kSecAttrGeneric = _str_symbol('kSecAttrGeneric')

# Password Attribute Keys (internet password only)
kSecAttrSecurityDomain = _str_symbol('kSecAttrSecurityDomain')
kSecAttrServer = _str_symbol('kSecAttrServer')
kSecAttrProtocol = _str_symbol('kSecAttrProtocol')
kSecAttrAuthenticationType = _str_symbol('kSecAttrAuthenticationType')
kSecAttrPort = _str_symbol('kSecAttrPort')
kSecAttrPath = _str_symbol('kSecAttrPath')

# kSecAttrProtocol values
kSecAttrProtocolFTP = _str_symbol('kSecAttrProtocolFTP')
kSecAttrProtocolFTPAccount = _str_symbol('kSecAttrProtocolFTPAccount')
kSecAttrProtocolHTTP = _str_symbol('kSecAttrProtocolHTTP')
kSecAttrProtocolIRC = _str_symbol('kSecAttrProtocolIRC')
kSecAttrProtocolNNTP = _str_symbol('kSecAttrProtocolNNTP')
kSecAttrProtocolPOP3 = _str_symbol('kSecAttrProtocolPOP3')
kSecAttrProtocolSMTP = _str_symbol('kSecAttrProtocolSMTP')
kSecAttrProtocolSOCKS = _str_symbol('kSecAttrProtocolSOCKS')
kSecAttrProtocolIMAP = _str_symbol('kSecAttrProtocolIMAP')
kSecAttrProtocolLDAP = _str_symbol('kSecAttrProtocolLDAP')
kSecAttrProtocolAppleTalk = _str_symbol('kSecAttrProtocolAppleTalk')
kSecAttrProtocolAFP = _str_symbol('kSecAttrProtocolAFP')
kSecAttrProtocolTelnet = _str_symbol('kSecAttrProtocolTelnet')
kSecAttrProtocolSSH = _str_symbol('kSecAttrProtocolSSH')
kSecAttrProtocolFTPS = _str_symbol('kSecAttrProtocolFTPS')
kSecAttrProtocolHTTPS = _str_symbol('kSecAttrProtocolHTTPS')
kSecAttrProtocolHTTPProxy = _str_symbol('kSecAttrProtocolHTTPProxy')
kSecAttrProtocolHTTPSProxy = _str_symbol('kSecAttrProtocolHTTPSProxy')
kSecAttrProtocolFTPProxy = _str_symbol('kSecAttrProtocolFTPProxy')
kSecAttrProtocolSMB = _str_symbol('kSecAttrProtocolSMB')
kSecAttrProtocolRTSP = _str_symbol('kSecAttrProtocolRTSP')
kSecAttrProtocolRTSPProxy = _str_symbol('kSecAttrProtocolRTSPProxy')
kSecAttrProtocolDAAP = _str_symbol('kSecAttrProtocolDAAP')
kSecAttrProtocolEPPC = _str_symbol('kSecAttrProtocolEPPC')
kSecAttrProtocolIPP = _str_symbol('kSecAttrProtocolIPP')
kSecAttrProtocolNNTPS = _str_symbol('kSecAttrProtocolNNTPS')
kSecAttrProtocolLDAPS = _str_symbol('kSecAttrProtocolLDAPS')
kSecAttrProtocolTelnetS = _str_symbol('kSecAttrProtocolTelnetS')
kSecAttrProtocolIMAPS = _str_symbol('kSecAttrProtocolIMAPS')
kSecAttrProtocolIRCS = _str_symbol('kSecAttrProtocolIRCS')
kSecAttrProtocolPOP3S = _str_symbol('kSecAttrProtocolPOP3S')

# kSecAttrAuthenticationType values
kSecAttrAuthenticationTypeNTLM = _str_symbol('kSecAttrAuthenticationTypeNTLM')
kSecAttrAuthenticationTypeMSN = _str_symbol('kSecAttrAuthenticationTypeMSN')
kSecAttrAuthenticationTypeDPA = _str_symbol('kSecAttrAuthenticationTypeDPA')
kSecAttrAuthenticationTypeRPA = _str_symbol('kSecAttrAuthenticationTypeRPA')
kSecAttrAuthenticationTypeHTTPBasic = _str_symbol('kSecAttrAuthenticationTypeHTTPBasic')
kSecAttrAuthenticationTypeHTTPDigest = _str_symbol('kSecAttrAuthenticationTypeHTTPDigest')
kSecAttrAuthenticationTypeHTMLForm = _str_symbol('kSecAttrAuthenticationTypeHTMLForm')
kSecAttrAuthenticationTypeDefault = _str_symbol('kSecAttrAuthenticationTypeDefault')

# https://developer.apple.com/documentation/security/keychain_services/keychain_items/item_return_result_keys?language=objc
kSecReturnData = _str_symbol('kSecReturnData')
kSecReturnAttributes = _str_symbol('kSecReturnAttributes')
kSecReturnRef = _str_symbol('kSecReturnRef')
kSecReturnPersistentRef = _str_symbol('kSecReturnPersistentRef')

# https://developer.apple.com/documentation/security/keychain_services/keychain_items/item_return_result_keys?language=objc
kSecValueData = _str_symbol('kSecValueData')
kSecValueRef = _str_symbol('kSecValueRef')
kSecValuePersistentRef = _str_symbol('kSecValuePersistentRef')

# https://developer.apple.com/documentation/security/keychain_services/keychain_items/search_attribute_keys_and_values?language=objc
kSecMatchLimit = _str_symbol('kSecMatchLimit')
kSecMatchLimitAll = _str_symbol('kSecMatchLimitAll')
kSecMatchLimitOne = _str_symbol('kSecMatchLimitOne')
kSecMatchCaseInsensitive = _str_symbol('kSecMatchCaseInsensitive')

# https://developer.apple.com/documentation/security/keychain_services/keychain_items/item_attribute_keys_and_values#1679100?language=objc
kSecAttrAccessibleAlways = _str_symbol('kSecAttrAccessibleAlways')
kSecAttrAccessibleAlwaysThisDeviceOnly = _str_symbol('kSecAttrAccessibleAlwaysThisDeviceOnly')
kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly = _str_symbol('kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly')
kSecAttrAccessibleAfterFirstUnlock = _str_symbol('kSecAttrAccessibleAfterFirstUnlock')
kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly = _str_symbol('kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly')
kSecAttrAccessibleWhenUnlocked = _str_symbol('kSecAttrAccessibleWhenUnlocked')
kSecAttrAccessibleWhenUnlockedThisDeviceOnly = _str_symbol('kSecAttrAccessibleWhenUnlockedThisDeviceOnly')

# https://developer.apple.com/documentation/security/secaccesscontrolcreateflags/ksecaccesscontroluserpresence
kSecAccessControlUserPresence = 1 << 0
kSecAccessControlTouchIDAny = 1 << 1
kSecAccessControlTouchIDCurrentSet = 1 << 3
kSecAccessControlDevicePasscode = 1 << 4
kSecAccessControlOr = 1 << 14
kSecAccessControlAnd = 1 << 15
kSecAccessControlPrivateKeyUsage = 1 << 30
kSecAccessControlApplicationPassword = 1 << 31

# https://developer.apple.com/documentation/security/ksecuseauthenticationuiallow?language=objc
kSecUseAuthenticationUI = _str_symbol('kSecUseAuthenticationUI')
kSecUseAuthenticationUIAllow = _str_symbol('kSecUseAuthenticationUIAllow')
kSecUseAuthenticationUIFail = _str_symbol('kSecUseAuthenticationUIFail')
kSecUseAuthenticationUISkip = _str_symbol('kSecUseAuthenticationUISkip')
kSecUseDataProtectionKeychain = _str_symbol('kSecUseDataProtectionKeychain')

kSecUseOperationPrompt = _str_symbol('kSecUseOperationPrompt')
kSecUseAuthenticationContext = _str_symbol('kSecUseAuthenticationContext')


#
# Security framework functions
#

CFTypeRef = c_void_p
CFDictionaryRef = c_void_p
SecAccessControlRef = c_void_p
CFErrorRef = c_void_p
CFAllocatorRef = c_void_p

# void CFRelease(CFTypeRef cf)
# https://developer.apple.com/documentation/corefoundation/1521153-cfrelease
CFRelease = c.CFRelease
CFRelease.restype = None
CFRelease.argtypes = [CFTypeRef]

# OSStatus SecItemAdd(CFDictionaryRef attributes, CFTypeRef  _Nullable *result);
# https://developer.apple.com/documentation/security/1401659-secitemadd?language=objc
SecItemAdd = c.SecItemAdd
SecItemAdd.restype = c_int
SecItemAdd.argtypes = [CFDictionaryRef, POINTER(CFTypeRef)]

# OSStatus SecItemUpdate(CFDictionaryRef query, CFDictionaryRef attributesToUpdate);
# https://developer.apple.com/documentation/security/1393617-secitemupdate?language=objc
SecItemUpdate = c.SecItemUpdate
SecItemUpdate.restype = c_int
SecItemUpdate.argtypes = [CFDictionaryRef, CFDictionaryRef]

# OSStatus SecItemCopyMatching(CFDictionaryRef query, CFTypeRef  _Nullable *result);
# https://developer.apple.com/documentation/security/1398306-secitemcopymatching?language=objc
SecItemCopyMatching = c.SecItemCopyMatching
SecItemCopyMatching.restype = c_int
SecItemCopyMatching.argtypes = [CFDictionaryRef, POINTER(CFTypeRef)]

# OSStatus SecItemDelete(CFDictionaryRef query);
# https://developer.apple.com/documentation/security/1395547-secitemdelete?language=objc
SecItemDelete = c.SecItemDelete
SecItemDelete.restype = c_int
SecItemDelete.argtypes = [CFDictionaryRef]

# SecAccessControlRef SecAccessControlCreateWithFlags(CFAllocatorRef allocator, CFTypeRef protection,
#                                                     SecAccessControlCreateFlags flags, CFErrorRef  _Nullable *error);
# https://developer.apple.com/documentation/security/1394452-secaccesscontrolcreatewithflags?language=objc
SecAccessControlCreateWithFlags = c.SecAccessControlCreateWithFlags
SecAccessControlCreateWithFlags.restype = SecAccessControlRef
SecAccessControlCreateWithFlags.argtypes = [CFAllocatorRef, CFTypeRef, c_ulong, POINTER(CFErrorRef)]

#
# Keychain errors
#

_status_error_classes = {}

def register_status_error(status=None):
    def decorator(cls):
        _status_error_classes[status] = cls
        return cls
    return decorator

class KeychainError(Exception):
    def __init__(self, *args, status=None):
        super().__init__(*args)
        self.status = status

@register_status_error(-25299)
class KeychainDuplicateItemError(KeychainError):
    pass

@register_status_error(-25300)
class KeychainItemNotFoundError(KeychainError):
    pass

@register_status_error(-25293)
class KeychainAuthFailedError(KeychainError):
    pass

@register_status_error(-128)
class KeychainUserCanceledError(KeychainError):
    pass

@register_status_error(-25308)
class KeychainUserInteractionNotAllowedError(KeychainError):
    pass

@register_status_error(-50)
class KeychainParamError(KeychainError):
    pass

@register_status_error()
class KeychainUnhandledError(KeychainError):
    pass

def error_class_with_status(status):
    return _status_error_classes.get(status, _status_error_classes[None])

def raise_status(status, *args):
    if status:
        raise error_class_with_status(status)(*args, status=status)

#
# Kind of human interface for security framework
#

class ItemClass(str, Enum):
    GENERIC_PASSWORD = kSecClassGenericPassword
    INTERNET_PASSWORD = kSecClassInternetPassword

class AuthenticationPolicy(IntFlag):
    USER_PRESENCE = kSecAccessControlUserPresence
    TOUCH_ID_ANY = kSecAccessControlTouchIDAny
    TOUCH_ID_CURRENT_SET = kSecAccessControlTouchIDCurrentSet
    DEVICE_PASSCODE = kSecAccessControlDevicePasscode
    OR = kSecAccessControlOr
    AND = kSecAccessControlAnd
    PRIVATE_KEY_USAGE = kSecAccessControlPrivateKeyUsage
    APPLICATION_PASSWORD = kSecAccessControlApplicationPassword

class Accessibility(str, Enum):
    ALWAYS = kSecAttrAccessibleAlways
    ALWAYS_THIS_DEVICE_ONLY = kSecAttrAccessibleAlwaysThisDeviceOnly
    WHEN_PASSCODE_SET_THIS_DEVICE_ONLY = kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly
    AFTER_FIRST_UNLOCK = kSecAttrAccessibleAfterFirstUnlock
    AFTER_FIRST_UNLOCK_THIS_DEVICE_ONLY = kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
    WHEN_UNLOCKED = kSecAttrAccessibleWhenUnlocked
    WHEN_UNLOCKED_THIS_DEVICE_ONLY = kSecAttrAccessibleWhenUnlockedThisDeviceOnly

class AuthenticationUI(str, Enum):
    ALLOW = kSecUseAuthenticationUIAllow
    FAIL = kSecUseAuthenticationUIFail
    SKIP = kSecUseAuthenticationUISkip

class AccessControl:
    def __init__(self, accessibility: Accessibility, flags: AuthenticationPolicy):
        self._accessibility = accessibility
        self._flags = flags
        self._sac = None

    @property
    def accessibility(self):
        return self._accessibility

    @property
    def flags(self):
        return self._flags

    @property
    def value(self):
        if not self._sac:
            sac = SecAccessControlCreateWithFlags(None, ns_from_py(self._accessibility.value), self._flags, None)

            if sac is None:
                raise KeychainError('Failed to create SecAccessControl object')

            self._sac = ObjCInstance(sac)
            ## CFRelease(sac)

        return self._sac

def reset_keychain():
    """Delete all data from the keychain (including the master password) after showing a confirmation dialog."""

    # Not a fan of this method :)
    raise NotImplementedError('Use Pythonista keychain.reset_keychain() if you really need it')


def sec_item_add(attributes: dict) -> None:
    raise_status(
        SecItemAdd(ns_from_py(attributes), None),
        'Failed to add keychain item'
    )

def sec_item_update(query_attributes, attributes_to_update) -> None:
    raise_status(
        SecItemUpdate(ns_from_py(query_attributes), ns_from_py(attributes_to_update)),
        'Failed to update keychain item'
    )

def sec_item_delete(query_attributes) -> None:
    raise_status(
        SecItemDelete(ns_from_py(query_attributes)),
        'Failed to delete keychain item'
    )

def get_services(service=None):
    """Return a list of all services and accounts that are stored in the keychain (each item is a 2-tuple)."""
    query = {}
    query[kSecClass] = kSecClassGenericPassword
    if service:
        query[kSecAttrService] = service
    query[kSecReturnAttributes] = True
    query[kSecReturnData] = False
    query[kSecMatchLimit] = kSecMatchLimitAll
    query[kSecUseAuthenticationUI] = AuthenticationUI.ALLOW
    ptr = sec_item_copy_matching(query)
    nsitems = NSArray(ptr.value)
    items = py_from_ns(nsitems)
    try:
        return [
            (x['svce'], x['acct'])
            for x in items
        ]
    except KeychainItemNotFoundError:
        # Compatibility - Pythonista returns empty List if there're no passwords
        return []

def get_attributes(service, account):
    query = {}
    query[kSecClass] = kSecClassGenericPassword
    query[kSecAttrService] = service
    query[kSecAttrAccount] = account
    query[kSecReturnAttributes] = True
    query[kSecReturnData] = False
    #query[kSecReturnData] = True
    #query[kSecAttrIsInvisible] = True
    query[kSecMatchLimit] = kSecMatchLimitOne
    #query[kSecMatchLimit] = kSecMatchLimitAll
    query[kSecUseAuthenticationUI] = AuthenticationUI.ALLOW

    """
    if prompt:
        query[kSecUseOperationPrompt] = prompt
    """

    try:
        ptr = sec_item_copy_matching(dict(query))
        pyresult = py_from_ns(NSDictionary(ptr.value))
    except KeychainItemNotFoundError:
        print('No generic password items')
        print(str(sys.exc_info()))
        return None
    CFRelease(ptr)
    return pyresult

def get_password(service, account, context=None):
    query = {}
    query[kSecClass] = kSecClassGenericPassword
    query[kSecAttrService] = service
    query[kSecAttrAccount] = account
    #query[kSecReturnAttributes] = True
    #query[kSecReturnData] = False
    query[kSecReturnData] = True
    #query[kSecAttrIsInvisible] = True
    query[kSecMatchLimit] = kSecMatchLimitOne
    #query[kSecMatchLimit] = kSecMatchLimitAll
    query[kSecUseAuthenticationUI] = AuthenticationUI.ALLOW
    if context:
        query[kSecUseAuthenticationContext] = context

    """
    if prompt:
        query[kSecUseOperationPrompt] = prompt
    """

    try:
        ptr = sec_item_copy_matching(dict(query))
        pyresult = py_from_ns(NSArray(ptr.value)).decode()
    except KeychainItemNotFoundError:
        print('No generic password items')
        return None
    CFRelease(ptr)
    return pyresult

def set_password(service, account, data, authentication=None):
    query = {}
    query[kSecClass] = kSecClassGenericPassword
    query[kSecAttrService] = service
    query[kSecAttrAccount] = account
    query[kSecUseAuthenticationUI] = AuthenticationUI.ALLOW
    attrs = {}
    attrs[kSecClass] = kSecClassGenericPassword
    attrs[kSecAttrService] = service
    attrs[kSecAttrAccount] = account
    attrs[kSecUseAuthenticationUI] = AuthenticationUI.ALLOW
    if authentication:
        if authentication == 'biometric':
            if is_available():
                attrs[kSecAttrAccessControl] = AccessControl(Accessibility.WHEN_UNLOCKED_THIS_DEVICE_ONLY, AuthenticationPolicy.TOUCH_ID_CURRENT_SET).value
            else:
                print("Biometrics not available")
                print("use authentication='any' instead")
                return
        else:
            attrs[kSecAttrAccessControl] = AccessControl(Accessibility.WHEN_UNLOCKED_THIS_DEVICE_ONLY, AuthenticationPolicy.USER_PRESENCE).value
        attrs[kSecUseDataProtectionKeychain] = True

    attrs[kSecValueData] = data.encode()

    try:
        sec_item_add(attrs)
    except KeychainDuplicateItemError:
        del attrs[kSecClass]
        del attrs[kSecUseAuthenticationUI]
        sec_item_update(query, attrs)

def delete_password(service, account):
    query = {}
    query[kSecClass] = kSecClassGenericPassword
    query[kSecAttrService] = service
    query[kSecAttrAccount] = account
    try:
        sec_item_delete(query)
    except Exception:
        pass
        #print(sys.exc_info())

def sec_item_copy_matching(query_attributes) -> ObjCInstance:
    ptr = CFTypeRef()
    raise_status(
        SecItemCopyMatching(ns_from_py(query_attributes), byref(ptr)),
        'Failed -to- get keychain item'
    )
    assert(ptr.value is not None)
    return ptr

def new_context():
    context = LAContext.new()
    context.touchIDAuthenticationAllowableReuseDuration = 10.0
    return context

def is_available():
    context = LAContext.new()
    available = bool(context.canEvaluatePolicy_error_(1, None))
    #  FaceID only available if NSFaceIDUsageDescription key is found in applications Info.plist file.
    if context.biometryType == 2:
        with open(os.path.join(os.path.dirname(sys.executable), "Info.plist"), mode="rb") as fp:
            _properties = plistlib.load(fp)
            faceID = _properties.get('NSFaceIDUsageDescription', None)
            if not faceID:
                print('Missing NSFaceIDUsageDescription key in Info.plist')
                return False

    return available

if __name__ == '__main__':
    delete_password('test', 'prompt')
    set_password('test', 'prompt', 'data 321', 'biometric')

    context = new_context()
    pwd = get_password('test', 'prompt', context)
    print(pwd)


