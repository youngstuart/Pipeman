import os
import platform
import distutils.dir_util as du
import sys
from io import BytesIO
import urllib2
from contextlib import closing
from zipfile import ZipFile
try:
    import maya.cmds as mc
except:
    pass

userScriptsDir = mc.internalVar(uad=True)
def installPath():
    """Returns installation path in users default maya/scripts location

    :return: Returns installation path starting from user scripts directory
    :rtype: str
    """

    if platform.system() == "Darwin":
        #mc.warning("OSX Installation untested...")
        return os.path.join(userScriptsDir, 'modules', 'Pipeman')


    elif platform.system() == "Linux":
        #mc.warning("Linux Installation untested...")
        return os.path.join(userScriptsDir, 'modules', 'Pipeman')


    elif platform.system() == "Windows":
        return os.path.join(userScriptsDir, 'modules', 'Pipeman')


def uninstall(src):
    """Recursivley deletes source directory

    :param src: Target directory to delete
    :type src: str
    :return: Returns True/False if directory removal was successful or not found
    :rtype: bool
    """
    if os.path.exists(src):
        try:
            du.remove_tree(src)
            return True
        except:
            return False
    else:
        return True

def download(src):
    """Downloads file from url to users temp directory

    :param src: Source URL to download from
    :type src: str
    :return: Returns file path to downloaded file
    :rtype: str
    """

    fileName = src.split('/')[-1]
    tmp = mc.internalVar(utd=True)
    tempFile = os.path.join(tmp, fileName)
    with open(tempFile, 'w') as fileWrite:
        fileWrite.write(urllib2.urlopen(src).read())
        print('{0} write successful'.format(tempFile))
     
    return tempFile

def install(src, dst):
    """unpacks zip file to destination.

    :param src: url to zip file
    :type src: str
    :param dst: Path to write zip file contents to
    :type dst: str
    :return: Returns root path of unpacked files
    :rtype: str
    """
    zipName = os.path.splitext(src)[0]
    with closing(ZipFile(src)) as zip:
        zip.extractall(zipName)
        unzipped_files = os.path.join(zipName, 'Pipeman-master')
        print('Unpack Successful: {0}'.format(unzipped_files))

        du.copy_tree(unzipped_files, dst)
        print('Copy successful: {0}'.format(dst))


    #clean up temp folder
    os.remove(src)
    uninstall(zipName)

def onMayaDroppedPythonFile(obj):
    src = 'https://github.com/youngstuart/Pipeman/archive/master.zip'
    dst = installPath()
    if uninstall(dst):
        zipFile = download(src)
        install(zipFile, dst)