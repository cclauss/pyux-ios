# -*- coding: utf-8 -*-
import sys, os, json, shutil, requests
from zipfile import ZipFile

"""
version 1.0
running the following line on your iOS device will extract demo.py and the examples folder to the current directory.
import requests as r; exec(r.get('https://raw.githubusercontent.com/sbbosco/pyux-ios/main/dist/get-uxdemo.py').content)
"""

if sys.platform == 'ios':
    if 'Pyto.app' in sys.executable:
        sitepath = os.path.expanduser('~/Documents/lib/python3.10/site-packages')
    else:
        sitepath = os.path.expanduser('~/Documents/site-packages')

    tmppath = os.environ.get('TMPDIR', os.environ.get('TMP', 'none'))
    if not os.path.exists(tmppath):
        tmppath = sitepath
else:
    sitepath = os.path.join(os.getcwd(), 'site-packages')
    tmppath = os.path.join(os.getcwd(), 'temp')


def get_examples():
    print('Get pyux-ios demo files...')
    url = 'https://raw.githubusercontent.com/sbbosco/pyux-ios/main/dist/uxdemo.zip'
    print(url)
    print(tmppath)
    r = requests.get(url)
    if r.status_code == 200:
        try:
            pkg_file = os.path.join(tmppath, 'uxdemo.zip')

            with open(pkg_file, 'wb') as f:
                f.write(r.content)
                print('download complete...')

        except:
            print("download error: ",str(sys.exc_info()))
            return

        with ZipFile(pkg_file, 'r') as zip:
            # extracting all the files
            print('Extracting all the files now...')
            zip.extractall()
            print('Done!')

        os.remove(pkg_file)
    else:
        print('download error...')

if os.path.exists(sitepath):
    get_examples()
else:
    print('Cannot locate site-packages directory!')
    print('Install aborted...')
