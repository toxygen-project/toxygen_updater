import os
import urllib.request
import os.path
import zipfile
import tarfile
import shutil
import sys
import subprocess
import platform


def update(url, version):
    log('URL: ' + str(url))

    curr = curr_directory()
    os.chdir(curr)
    file_name = url[url.rindex('/') + 1:]
    full_file_name = curr + '/' + file_name
    urllib.request.urlretrieve(url, full_file_name)

    if file_name.endswith('.zip'):
        with zipfile.ZipFile(full_file_name) as z:
            z.extractall(curr)
    else:
        with tarfile.TarFile(full_file_name) as z:
            z.extractall(curr)
    log('Archive extracted')

    folder = 'toxygen-{}'.format(version)
    from_sources = True
    if not os.path.exists(folder):
        os.rename('toxygen', folder)
        from_sources = False
    folder = curr + '/' + folder

    if not from_sources:
        copy(folder, curr)
    else:
        copy(folder, os.path.abspath(os.path.join(curr, os.pardir)))

    os.remove(full_file_name)
    shutil.rmtree(folder)
    log('Installation finished')

    if from_sources:
        params = 'python3 main.py'
    elif platform.system() == 'Windows':
        params = curr + '/toxygen.exe'
    else:
        params = './toxygen'

    try:
        subprocess.Popen(params)
    except Exception as ex:
        log('Exception: running Toxygen failed with ' + str(ex))


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
    if len(sys.argv) == 3:
        download_url = sys.argv[1]
        new_version = sys.argv[2]
        update(download_url, new_version)
    else:
        print('Usage: toxygen_updater <url> <target_version>')
