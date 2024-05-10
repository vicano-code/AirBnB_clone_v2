#!/usr/bin/python3
"""
distributes an archive to your web servers
Returns False if the file at the path archive_path doesn’t exist
Returns True if all operations have been done correctly, otherwise return False
Usage:
    fab -f 2-do_deploy_web_static.py do_deploy:archive_path=
    versions/web_static_20170315003959.tgz -i my_ssh_private_key -u ubuntu
"""
from fabric.api import env, put, run
import os


env.hosts = ['54.157.179.15', '100.25.30.122']


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
