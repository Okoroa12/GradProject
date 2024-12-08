from scapy.all import sniff # type: ignore
import subprocess

IP_MAC_Map = {}
def processpacket(packet):
    src_ip = packet['ARP'].psrc
    src_mac = packet['Ether'].src

    if src_mac in IP_MAC_Map.keys():
        if IP_MAC_Map[src_mac] != src_ip:
            old_ip = IP_MAC_Map[src_mac]
            print(f"Possible ARP attack detected: {old_ip} is pretending to be {src_ip}")
            block_ip(src_ip)
    else:
        IP_MAC_Map[src_mac] = src_ip

def block_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP {ip}: {e}")

sniff(filter="arp", store=0, prn=processpacket, iface="eth0")
