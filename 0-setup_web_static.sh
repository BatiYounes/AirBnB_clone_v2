#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static.

apt update
apt install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring

curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
| sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/mainline/ubuntu `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    | sudo tee /etc/apt/preferences.d/99nginx

apt update
apt -y install nginx

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
chown -R ubuntu /data/
chgrp -R ubuntu /data/
ln -sf /data/web_static/releases/test/ /data/web_static/current

rm /etc/nginx/conf.d/default.conf

printf %s "<html>
	<head>
	</head>
	<body>
		Holberton School
	</body>
</html>" > /data/web_static/releases/test/index.html

printf %s "server {
	listen 80 backlog=4096 default_server;
	#server_name  web-01.dakhamed-dom.tech;
	add_header X-Served-By "$HOSTNAME";
	
	location / {
		root /home/ubuntu/projects/web_app/alx/html;
		index  index.html;
	}
	
	error_page  404              /404.html;

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html;
	}

	error_page   500 502 503 504  /50x.html;
	location = /50x.html {
		root   /usr/share/nginx/html;
	}
}" > /etc/nginx/conf.d/default.conf

sysctl -w net.core.somaxconn=4096
echo "net.core.somaxconn = 4096" >> /etc/sysctl.conf

service nginx restart
