#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
import os

env.hosts = ['52.7.166.204', '52.91.146.234']  # IPs of your web servers
env.user = 'ubuntu'  # SSH username
env.key_filename = '~/.ssh/new_key'  # Path to your SSH private key


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract archive filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_basename = archive_filename.split(".")[0]

        # Upload archive to /tmp/ directory on web server
        put(archive_path, "/tmp/{}".format(archive_filename))

        # Create target directory
        run("mkdir -p /data/web_static/releases/{}/".format(archive_basename))

        # Uncompress the archive to the folder
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(archive_filename, archive_basename))

        # Remove the uploaded archive
        run("rm /tmp/{}".format(archive_filename))

        # Move contents from web_static to the parent directory
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(archive_basename, archive_basename))

        # Remove the now-empty web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_basename))

        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(archive_basename))

        # Set permissions
        run("chmod -R 755 /data/web_static/releases/{}/".format(archive_basename))

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
