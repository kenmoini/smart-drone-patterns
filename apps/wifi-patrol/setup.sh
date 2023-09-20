#!/bin/bash

mkdir -p /opt/wifi-patrol

cp nmcli-wrapper.sh /opt/wifi-patrol/nmcli-wrapper.sh
chmod a+x /opt/wifi-patrol/nmcli-wrapper.sh

cp wifi-patrol.service /etc/systemd/system/wifi-patrol.service

chmod 644 /etc/systemd/system/wifi-patrol.service
chown root:root /etc/systemd/system/wifi-patrol.service

systemctl enable --now wifi-patrol.service
