#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from the contents of the
web_static folder of my AirBnB Clone repo, using the function do_pack
    Prototype: def do_pack():
All files in the folder web_static are  added to the final archive
All archives are stored in the folder versions (the function creates this
folder if it doesn’t exist)
The name of the archive created must be:
    web_static_<year><month><day><hour><minute><second>.tgz
Returns the archive path if correctly generated. Otherwise, return None
Usage: fab -f 1-pack_web_static.py do_pack
"""
from fabric.api import local
from datetime import datetime


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
