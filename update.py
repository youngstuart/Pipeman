import os
import platform
import distutils.dir_util as du
import sys
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
try:
    from maya import mc
except:
    pass


def installPath():
    """Returns installation path in users default maya/scripts location

    :return: Returns installation path starting from user scripts directory
    :rtype: str
    """
    userScriptsDir = mc.internalVar(usd=True)

    if platform.system() == "Darwin":
        #mc.warning("OSX Installation untested...")
        return os.path.join(userScriptsDir, 'Pipeman')


    elif platform.system() == "Linux":
        #mc.warning("Linux Installation untested...")
        return os.path.join(userScriptsDir, 'Pipeman')


    elif platform.system() == "Windows":
        return os.path.join(userScriptsDir, 'Pipeman')


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
        Return True

def install(src, dst):
    """Downloads and unpacks zip file to destination.

    :param src: url to zip file
    :type src: str
    :param dst: Path to write zip file contents to
    :type dst: str
    :return: Returns root path of unpacked files
    :rtype: str
    """
    with urlopen(src) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(dst)


def onMayaDroppedPythonFile(obj):
    src = 'https://github.com/youngstuart/Pipeman/archive/master/zip'
    dst = installPath()
    if uninstall(dst):
        install(src, dst)