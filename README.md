# arpspoofpy

**Easy ARP spoofer** - simple ARP spoofing script for local networks.

![status](https://img.shields.io/badge/status-experimental-orange) ![python](https://img.shields.io/badge/python-3.8%2B-blue)

---

## ⚠️ Legal
Use **only** in a lab or on systems you own/have permission to test. Unauthorized use is illegal.

---

## Requirements
- Python 3.8+
- root privileges
## Guide
- echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
- ip a
- sudo python3 arpSpoof.py <Victim_IP> <Your_IP>
