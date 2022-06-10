systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd

apt install mosquitto

echo -e "listener 1883 \nallow_anonymous true" >> /etc/mosquitto/mosquitto.conf

reboot