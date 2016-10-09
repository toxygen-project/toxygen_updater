try:
    from PySide import QtNetwork
except ImportError:
    from PyQt4 import QtNetwork
import sys
import urllib.request
import os.path
import zipfile
import gzip


def update(url):
    log('URL: ' + str(url))
    req = urllib.request.urlopen(url)
    data = req.read()
    file_name = url[url.rindex('/') + 1:]
    with open(file_name, 'wb') as fl:
        fl.write(data)
    if file_name.endswith('.zip'):
        with zipfile.ZipFile(curr_directory() + '/' + file_name) as z:
            z.extractall(curr_directory())
    # TODO: extract tar.gz and to curr folder


def log(data):
    with open(curr_directory() + '/updater_logs.log', 'a') as fl:
        fl.write(str(data) + '\n')


def curr_directory():
    return os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        update(url)
