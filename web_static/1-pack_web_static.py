#!/usr/bin/python3
'''Module containing do_pack'''
import os.path as path
from datetime import datetime
from fabric.api import local


def do_pack():
    '''generates a .tgz archive from the contents of the web_static folder'''
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    file = "versions/web_static_{}.tgz".format(now)

    if path.isdir("versions") is False:
        if local("mkdir -p versions").failed:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed:
        return None
    return file
