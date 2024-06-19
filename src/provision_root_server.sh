echo "Hej from FreeBSD"
ntpdate dk.pool.ntp.org

echo "Installing package system..."
pkg bootstrap

echo "Setting hostname..."
sed -i '' 's/hostname="rpi-b"/\hostname="rpi-b-server"/' /etc/rc.conf

pkg install -y nano

echo "Setting up BASH as default shell..."
pkg install -y bash

chsh -s /usr/local/bin/bash freebsd

echo "Installing PyENV..."
pkg install -y pyenv
eval "$(pyenv init -)"
pkg install -y python3

# This one is needed to make the Python build scripts find the respective libraries
pkg install -y pkgconf

# Needed to install Python 3.13-dev
pkg install -y git
pkg install -y wget

#pkg install -y nginx

echo "Installing Pythons..."
pkg install -y python2-2_3
pkg install -y python27-2.7.18_2
pkg install -y python3-3_3

pkg install -y python38 py38-sqlite3
pkg install -y python39 py39-sqlite3
pkg install -y python310 py310-sqlite3
pkg install -y python311 py311-sqlite3
