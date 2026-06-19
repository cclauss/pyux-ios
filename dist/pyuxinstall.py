# -*- coding: utf-8 -*-
import sys, os, json, shutil, requests
from zipfile import ZipFile

"""
version 1.0
install by running the following line on iOS device:
import requests as r; exec(r.get('https://raw.githubusercontent.com/sbbosco/pyux-ios/main/dist/pyuxinstall.py').content)
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

def download_info(pkg_name):
    r = requests.get("https://pypi.python.org/pypi/{}/json".format(pkg_name))
    if r.status_code == 200:
        info = r.json()["info"]
        url = r.json()["urls"][0]["url"]
        print(url)
        return url
    else:
        return None

def download_pkg(url, dest_path):
    r = requests.get(url)
    if r.status_code == 200:
        with open(dest_path, 'wb') as f:
            f.write(r.content)
            print('download complete...')


def install_pkg(pkg_file):
    savepath = os.getcwd()
    os.chdir(sitepath)
    with ZipFile(pkg_file, 'r') as zip:
        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall()
        print('Done!')

    os.remove(pkg_file)
    os.chdir(savepath)

def get_pyux():
    print('Installing pyux-ios...')
    url = 'https://raw.githubusercontent.com/sbbosco/pyux-ios/main/dist/pyux_ios-1.0.1-py3-none-any.whl'
    print(url)
    r = requests.get(url)
    if r.status_code == 200:
        savepath = os.getcwd()
        try:
            pkg_file = os.path.join(tmppath, 'pyux.zip')
            with open(pkg_file, 'wb') as f:
                f.write(r.content)
                print('download complete...')
        except:
            print("PyUx download error: ",str(sys.exc_info()))
            return

        dirlist = os.listdir(sitepath)
        for f in dirlist:
            if f.split('-')[0] == 'pyux_ios':
                shutil.rmtree(os.path.join(sitepath, f))
            if f == 'ux':
                shutil.rmtree(os.path.join(sitepath, f))

        os.chdir(sitepath)
        with ZipFile(pkg_file, 'r') as zip:
            # extracting all the files
            print('Extracting all the files now...')
            zip.extractall()
            print('Done!')

        os.remove(pkg_file)
        os.chdir(savepath)
    else:
        print('PyUx download error...')

if os.path.exists(sitepath):

    try:
        import rubicon.objc
    except:
        print('Installing rubicon-objc...')
        pkg_name = 'rubicon-objc'
        url = download_info(pkg_name)
        dest_path = os.path.join(tmppath, pkg_name + '.zip')
        download_pkg(url, dest_path)
        install_pkg(dest_path)

    get_pyux()

else:
    print('Cannot locate site-packages directory!')
    print('Install aborted...')
