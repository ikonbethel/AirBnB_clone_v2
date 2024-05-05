#!/usr/bin/env bash
# Prepares web servers for deployment of web_static

# Create required directories
rm -rf /data/web_static/releases/test/ /data/web_static/shared/
mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# Create dummy index page
tee /data/web_static/releases/test/index.html <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create Symbolic Link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update and Upgrade
apt-get -y update
apt-get -y upgrade

# Install nginx on your web server
# Nginx should be listening on port 80
if ! command -v nginx &> /dev/null; then
	apt-get -y install nginx
fi

HOSTNAME=$(hostname)

cp -n /var/www/html/index.nginx-debian.html /var/www/html/index_bckup
echo "Hello World!" > /var/www/html/index.nginx-debian.html
echo "Ceci n'est pas une page" > /var/www/html/404.html
cp -n /etc/nginx/sites-available/default /etc/nginx/sites-available/default_backup

# Nginx Config
tee /etc/nginx/sites-available/default <<EOF
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
	index index.html index.htm index.nginx-debian.html;
	server_name _;

	location /redirect_me {
		return 301 https://www.google.com;
	}

	error_page 404 /404.html;

	location /404 {
		root /var/www/html;
		internal;
	}

	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html test/index.html;
	}

	# Add custom header
	add_header X-Served-By "$HOSTNAME";
}
EOF

# Check for syntax errors
nginx -t

# Restart Nginx
service nginx restart
