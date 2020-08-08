import os
import platform
import distutils.dir_util as du
import distutils.file_util as fu
import sys
from io import BytesIO
import urllib2
from contextlib import closing
from zipfile import ZipFile
# Wrapping Maya specific module to prevent Sphinx Importerror
try:
    import maya.cmds as mc
except:
    pass

userAppDir = mc.internalVar(uad=True)
def installPath(src):
    """Returns installation path in default user application directory

    :param src: URL to github public repository zip
    :type src: str
    :return: Returns installation path starting from default user application directory
    :rtype: str
    """
    # github zip URL is structured ['https:', '', 'github.com', <account>, <repo>, 'archive', 'master.zip']
    repoName = src.split('/')[-3]
    if platform.system() == "Darwin":
        #mc.warning("OSX Installation untested...")
        return os.path.join(userAppDir, 'modules', repoName)


    elif platform.system() == "Linux":
        #mc.warning("Linux Installation untested...")
        return os.path.join(userAppDir, 'modules', repoName)


    elif platform.system() == "Windows":
        return os.path.join(userAppDir, 'modules', repoName)


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
    modulePath = os.path.dirname(dst)
    assert (os.path.exists(modulePath)) 'Target destination:\n{0}\ndoes not exist'.format(modulePath)
    # zipDst = zip file path without .zip extension
    zipDst = os.path.splitext(src)[0]
    zipName = os.path.basename(zipDst)
    modName = '{0}.mod'.format(zipName.split('-'))
    with closing(ZipFile(src)) as zip:
        # extract to same directory as zip file with same name as file
        zip.extractall(zipDst)
        # github zip files are structured as:
        # repo-master.zip > repo-master > contents
        unzipped_files = os.path.join(zipDst, zipName)
        mod_file = os.path.join(unzipped_files, 'src', modName)
        print('Unpack Successful: {0}'.format(unzipped_files))

        du.copy_tree(unzipped_files, dst)
        fu.copy_file(mod_file, modulePath)
        print('Copy successful: {0}'.format(dst))


    #clean up temp folder
    os.remove(src)
    uninstall(zipDst)

def onMayaDroppedPythonFile(obj):
    """Special Maya function, not much information on it.  Maya tries to run this function when a .py file is dropped on the viewport

    :param obj: Unknown parameter Maya passes
    :returns: None
    :rtype: null
    """

    src = 'https://github.com/youngstuart/Pipeman/archive/master.zip'
    dst = installPath(src)
    if uninstall(dst):
        zipFile = download(src)
        install(zipFile, dst)