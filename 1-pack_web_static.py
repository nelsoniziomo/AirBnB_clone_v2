#!/usr/bin/python3

""" A Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Create a .tgz archive from web_static folder
    """
    # Create versions directory if it doesn't exist
    if not os.path.exists("versions"):
        local("mkdir versions")

    # Create tgz file with date and time format
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    tgz_file = "versions/web_static_{}.tgz".format(now)

    # Create the archive
    try:
        local("tar -cvzf {} web_static".format(tgz_file))
        return tgz_file
    except:
        return None
