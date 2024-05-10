#!/usr/bin/python3
"""
Fabric script methods:
    do_pack: packs web_static/ files into .tgz archive
    do_deploy: deploys archive to webservers
    deploy: do_packs && do_deploys
Usage:
    fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
"""
from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['54.157.179.15', '100.25.30.122']


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""

    now = datetime.now().strftime("%Y%M%d%H%M%S")
    local("mkdir -p versions")
    archive_name = "web_static_{}.tgz".format(now)
    archive_path = "versions/{}".format(archive_name)
    result = local("tar -czvf {} web_static".format(archive_path))
    if result.succeeded:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """Deploy archive to web servers"""

    # check if archive_path exists
    if not os.path.exists(archive_path):
        return False

    try:
        # upload archive to /tmp/ directory on web server
        put(archive_path, '/tmp/')

        # get archive filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_filename_without_ext = archive_filename.split('.')[0]

        # uncompress the archive into the folder:
        # /data/web_static/releases/<archive filename without extension>
        release_folder = '/data/web_static/releases/{}/'.format(
                         archive_filename_without_ext)
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # delete archive from web server
        run('rm -f /tmp/{}'.format(archive_filename))

        run('mv {}web_static/* {}'.format(release_folder, release_folder))

        run('rm -rf {}web_static'.format(release_folder))

        # delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # create new symbolic link /data/web_static/current linked to the
        # new version
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print("new version deployed")
        return True
    except Exceotion as e:
        print("An error occured:", str(e))
        return False


def deploy():
    """create and deploys archives to servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    result = do_deploy(archive_path)
    return result
