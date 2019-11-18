# At 1and1 control panel change 
@ record for aidataviz.com root domain to host ip address
A record for www subdomain to host ip address

# based on https://github.com/diafygi/acme-tiny

# Create a Let's Encrypt account private key 
openssl genrsa 4096 > account.key

# Generate a domain private key
openssl genrsa 4096 > domain.key

# single domain
openssl req -new -sha256 -key domain.key -subj "/CN=batnetwork.org" > domain.csr

openssl req -new -sha256 -key domain.key -subj "/CN=aidataviz.com" > domain.csr

# For multiple domains (use this one if you want both www.yoursite.com and yoursite.com)
openssl req -new -sha256 -key domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:batnetwork.com,DNS:www.aidataviz.com")) > domain.csr

# Make some challenge folder (modify to suit your needs)
mkdir -p /var/www/challenges/

# install nginx
sudo apt install nginx-light

# make config
sudo nano -w /etc/nginx/sites-enabled/batnetwork.org

/var/log/nginx/access.log
less /var/log/nginx/error.log 

# write config
server {
    listen 80;
    server_name batnetwork.org;
    #https redirect
    return 301 https://$host$request_uri;
    location /.well-known/acme-challenge/ {
        alias /var/www/challenges/;
        try_files $uri =404;
    }
}

server {
    listen 443 ssl;
    server_name batnetwork.org;

    ssl_certificate /home/ubuntu/ssl/signed_chain.crt;
    ssl_certificate_key /home/ubuntu/ssl/domain.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA;
    ssl_session_cache shared:SSL:50m;
#   ssl_dhparam ~/ssl/server.dhparam;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
    location /BATLAS {
      proxy_pass http://localhost:3838/BATLAS;
    }
    location /gwas {
      proxy_pass http://localhost:8001;
    }
   root /home/ubuntu/test;
   index index.html;


}

wget https://raw.githubusercontent.com/diafygi/acme-tiny/master/acme_tiny.py
# get ssl certificate
# Run the script on your server
sudo systemctl restart nginx
python acme_tiny.py --account-key account.key --csr domain.csr --acme-dir /var/www/challenges/ > signed_chain.crt

# use the www.aidataviz.com nginx config file

# check test flask app
gunicorn test:app &> test.log &

# renew cert: Example of a renew_cert.sh:
#!/usr/bin/sh
cd ~/ssl
python acme_tiny.py --account-key account.key --csr domain.csr --acme-dir /var/www/challenges/ > signed_chain.crt
service nginx reload

# Example line in your crontab (runs end of every month) edit /etc/crontab
0 0 28 * * ~/ssl/renew_cert.sh 2>> /var/log/acme_tiny.log

# restart nginx 
sudo systemctl restart nginx

sudo gunicorn --certfile=/home/ubuntu/ssl/signed_chain.crt --keyfile=/home/ubuntu/ssl/domain.key new:server -b 0.0.0.0:443 

gunicorn new:server -b 127.0.0.1:8000 &>new.log &
gunicorn app1:server -b localhost:8001 &>log &
