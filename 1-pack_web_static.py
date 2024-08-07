#!/usr/bin/python3
# Fabric script to generate a .tgz archive from the web_static folder

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns:
        str: The archive path if the archive has been correctly generated,
             otherwise None.
    """
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None
