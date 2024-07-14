#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import env, put, run
import os

env.hosts = ['52.7.166.204', '52.91.146.234']  # Replace with your web' IPs
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    Args:
        archive_path (str): The path to the archive to distribute.
    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Get the archive file name without the extension
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split('.')[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Create the directory to uncompress the archive
        release_path = '/data/web_static/releases/{}'.format(no_ext)
        run('mkdir -p {}'.format(release_path))

        # Uncompress the archive to the folder
        run('tar -xzf /tmp/{} -C {}'.format(file_name, release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))

        # Move the contents out of the web_static folder to parent directory
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Delete the web_static directory created by the archive extraction
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_path))

        return True
    except Exception:
        return False
