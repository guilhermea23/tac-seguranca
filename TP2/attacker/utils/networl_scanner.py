#!/usr/bin/env python3
from scapy.all import ARP, Ether, srp


def scan_network(ip_range):
    print(f"[*] Scanning network {ip_range}")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices


if __name__ == "__main__":
    network = "172.20.0.1/24"  # Sub-rede do Docker
    devices = scan_network(network)

    print("Dispositivos na rede:")
    for device in devices:
        print(f"IP: {device['ip']}\tMAC: {device['mac']}")
