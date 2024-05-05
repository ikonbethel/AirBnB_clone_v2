#!/usr/bin/python3
'''Module containing do_pack'''
import os.path as path
from datetime import datetime
from fabric.api import local, put, env, run

env.hosts = [
    '100.26.236.251',
    '54.236.47.141'
]


def do_pack():
    '''generates a .tgz archive from the contents of the web_static folder'''
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    file = "versions/web_static_{}.tgz".format(now)

    if path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    '''distributes an archive to your web servers'''
    if path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    file_name = file.split(".")[0]
    if put(archive_path, f"/tmp/{file}").failed:
        return False
    target_dir = "/data/web_static/releases/{}/".format(file_name)

    if run("rm -rf {}".format(target_dir)).failed:
        return False
    if run("mkdir -p {}".format(target_dir)).failed:
        return False
    if run("tar -xzf /tmp/{} -C {}".format(file, target_dir)).failed:
        return False
    if run("mv -f {}web_static/* {}".format(target_dir, target_dir)).failed:
        return False
    if run("rm -rf {}web_static/".format(target_dir)).failed:
        return False
    if run("rm -f /tmp/{}".format(file)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s {} /data/web_static/current".format(target_dir)).failed:
        return False
    return True


def deploy():
    '''creates and distributes an archive to your web servers.'''
    archive_path = do_pack()
    if archive_path is None:
        return False
    return (do_deploy(archive_path))
