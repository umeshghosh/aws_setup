# disable auto ubuntu update
edit sudo nano /etc/apt/apt.conf.d/20auto-upgrades

APT::Periodic::Update-Package-Lists "0";

APT::Periodic::Unattended-Upgrade "0";

sudo apt update

sudo apt install python3-pip

sudo pip3 install dash dash_auth pandas

# enable_https
Enable Free https in website

# lifelines
