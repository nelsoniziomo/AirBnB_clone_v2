#!/usr/bin/python3
"""Deploy web static package
"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['52.87.219.241', '54.242.162.151']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """Deploy web files to server
    """
    if not path.exists(archive_path):
        return False

    filename = archive_path.split("/")[-1]
    name = filename.split(".")[0]

    with settings(abort_exception=Exception):
        try:
            # upload archive
            put(archive_path, "/tmp/")

            # create target dir
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            run(f"sudo mkdir -p /data/web_static/releases/{name}/")

            # uncompress archive and delete .tgz
            run(f"sudo tar -xzf /tmp/{filename} -C /data/web_static/releases/{name}/")

            # remove archive
            run(f"sudo rm /tmp/{filename}")

            # move contents into host web_static
            run(f"sudo mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/")

            # remove extraneous web_static dir
            run(f"sudo rm -rf /data/web_static/releases/{name}/web_static")

            # delete pre-existing sym link
            if run("sudo test -L /data/web_static/current").succeeded:
                run("sudo rm /data/web_static/current")

            # re-establish symbolic link
            run(f"sudo ln -s /data/web_static/releases/{name}/ /data/web_static/current")
        except Exception as e:
            print(f"Exception: {e}")
            return False

    return True
