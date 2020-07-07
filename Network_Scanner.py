#!/usr/bin/env python

import scapy.all as scapy
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Range of ip address to discover in the network")
    (option, arguments) = parser.parse_args()
    if not option.target:
        parser.error("\n[-] Please specify the target ip, use --help for more info")
    return option


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for elements in answered_list:
        clients_dict = {"ip": elements[1].psrc, "mac": elements[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC address")
    print("-------------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


target_ips = get_arguments().target
scan_result = scan(target_ips)
print_result(scan_result)
