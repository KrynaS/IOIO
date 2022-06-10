apt update
apt upgrade
apt install hostapd
apt-get install dnsmasq
cp hostapd.conf /etc/hostapd/
cp hostapd /etc/default/
cp dhcpd.conf /etc/
cp dnsmasq.conf /etc/
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
reboot