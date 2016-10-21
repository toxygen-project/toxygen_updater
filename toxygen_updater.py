try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui
import sys
import urllib.request
import os.path
import zipfile
import tarfile
import shutil
# TODO: add GUI


def update(url, version):
    log('URL: ' + str(url))
    req = urllib.request.urlopen(url)
    data = req.read()
    file_name = url[url.rindex('/') + 1:]
    curr = curr_directory()
    full_file_name = curr + '/' + file_name
    with open(file_name, 'wb') as fl:
        fl.write(data)
    if file_name.endswith('.zip'):
        with zipfile.ZipFile(full_file_name) as z:
            z.extractall(curr)
    else:
        with tarfile.TarFile(full_file_name) as z:
            z.extractall(curr)
    folder = 'toxygen-{}'.format(version)
    copy(folder, os.path.abspath(os.path.join(curr, os.pardir)))
    os.remove(full_file_name)
    shutil.rmtree(folder)
    log('Installation finished')


def log(data):
    with open(curr_directory() + '/updater_logs.log', 'a') as fl:
        fl.write(str(data) + '\n')


def curr_directory():
    return os.path.dirname(os.path.realpath(__file__))


def copy(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)
        else:
            copy(full_file_name, os.path.join(dest, file_name))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        url = sys.argv[1]
        version = sys.argv[2]
        update(url, version)
