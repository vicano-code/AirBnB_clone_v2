#!/usr/bin/env bash
# sets up web servers for the deployment of web_static
# Install Nginx if it not already installed
# create the below folders if they don't exist:
# 	/data/
# 	/data/web_static/
# 	/data/web_static/releases/
# 	/data/web_static/shared/
# 	/data/web_static/releases/test/
# create a test HTML file with simple content:
#	/data/web_static/releases/test/index.html
# create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/
# If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
# Give ownership of the /data/ folder to the ubuntu user AND group. This should be recursive; everything inside
# should be created/owned by this user/group.
# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
#	eg: https://mydomainname.tech/hbnb_static
# 	use alias in the configuration
# restart nginx
# Note: run script on your web servers

sudo apt-get  update
sudo apt-get -y upgrade
sudo apt-get install -y nginx
sudo service nginx start

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "fake content" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/

ADD_WEBSTATIC_CONFIG="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "34i $ADD_WEBSTATIC_CONFIG" /etc/nginx/sites-available/default

sudo service nginx restart
