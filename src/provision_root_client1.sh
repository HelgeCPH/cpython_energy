echo "Hej from FreeBSD"
ntpdate dk.pool.ntp.org

echo "Installing package system..."
pkg bootstrap

echo "Setting hostname..."
sed -i '' 's/hostname="rpi-b"/\hostname="rpi-b-client1"/' /etc/rc.conf

pkg install -y nano

echo "Setting up BASH as default shell..."
pkg install -y bash

chsh -s /usr/local/bin/bash freebsd

echo "Installing Pythons..."
pkg install -y python3
pkg install -y python3-3_3
pkg install -y python3-pip
pkg install -y py39-pip