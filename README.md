# arpspoofpy

Easy ARP spoofer

Guide:
echo 1 > /proc/sys/net/ipv4/ip_forward
ip a
python3 arpSpoof.py {Victim's IP} {Your IP}
