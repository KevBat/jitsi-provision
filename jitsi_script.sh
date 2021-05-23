#!/bin/bash

DOMAIN=$1
EMAIL=$2

#basic installs
apt update
apt install -y apt-transport-https debconf-utils curl gnupg2 nginx-full openjdk-8-jre-headless openssl python3-certbot-nginx
apt-add-repository universe
curl https://download.jitsi.org/jitsi-key.gpg.key | sudo sh -c 'gpg --dearmor > /usr/share/keyrings/jitsi-keyring.gpg'
echo 'deb [signed-by=/usr/share/keyrings/jitsi-keyring.gpg] https://download.jitsi.org stable/' | sudo tee /etc/apt/sources.list.d/jitsi-stable.list > /dev/null
apt update

#setup fqdn and hostname
hostnamectl set-hostname $DOMAIN
ip=$(ifconfig eth0 | perl -ne 'print $1 if /inet\s.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b/')
sed -i "s/^127.0.0.1 localhost/127.0.0.1 localhost\n$ip $DOMAIN/g" /etc/hosts

#firewall
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 10000/udp
ufw allow 22/tcp
ufw allow 3478/udp
ufw allow 5349/tcp
echo "y" | ufw enable
echo $(ufw status verbose)

#automate jitsi prompt settings and install
echo "jitsi-videobridge2 jitsi-videobridge/jvb-hostname string $DOMAIN" | debconf-set-selections
echo "jitsi-meet jitsi-meet/cert-choice select Self-signed certificate will be generated" | debconf-set-selections
export DEBIAN_FRONTEND="noninteractive"
apt install -y jitsi-meet

#install let's encrypt certificate
echo "$EMAIL" | /usr/share/jitsi-meet/scripts/install-letsencrypt-cert.sh

#TODO: setup access controls
#https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-quickstart#access-control