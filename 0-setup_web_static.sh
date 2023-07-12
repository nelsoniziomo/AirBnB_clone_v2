#!/usr/bin/env bash
# This script sets up the web server for deployment of web_static

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

# Create directory structure for web_static deployment
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html

# Create a fake HTML file to test Nginx configuration
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link /data/web_static/current linked to /data/web_static/releases/test/
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /data/web_static/current/ to hbnb_static
sudo sed -i "/listen 80 default_server;/a location /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default

# Restart Nginx to apply configuration changes
sudo service nginx restart
