#!/usr/bin/env python

import scapy.all as scapy


def scan(ip):
    # scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)   # Creating ARP packet with ip's
    # print(arp_request.summary())
    # print(scapy.ls(scapy.ARP()))  // Listing things we can set (options)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    # arp_request.show()  // To show details
    # broadcast.show()    // To show details
    # arp_request_broadcast.show()  # To show details
    # answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1)  # Sent packets and receive response or
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]  # we don't want unanswered list
    print(answered_list.summary())


scan("10.0.2.1/24")
