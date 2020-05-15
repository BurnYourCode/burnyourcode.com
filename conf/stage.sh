#!/bin/bash
set -e

website=oxal.org
rootDir=$HOME/$website
nginxConf=$website.conf

# First time set up root directory
if [ ! -d "$rootDir" ]; then
    echo "Setting up first time directories.."
    sudo mkdir -p $rootDir
    sudo chown -R `whoami`:www-data $rootDir
    cd $rootDir
    echo "Rsync now and run this again"
    exit
fi

# Copy nginx conf
sudo cp $rootDir/conf/$nginxConf /etc/nginx/sites-available/$nginxConf

# Create nginx conf symlink if it does not exists
# -h is for checking symlinks
if [ ! -h "/etc/nginx/sites-enabled/$nginxConf" ]; then
    sudo ln -s /etc/nginx/sites-available/$nginxConf /etc/nginx/sites-enabled/$nginxConf
fi

# reload nginx
sudo nginx -t && \
    sudo nginx -s reload || \
    echo "Error in configuration / nginx"
