#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_MAC", help="new_MAC to change MAC address")
    (option, arguments) = parser.parse_args()
    if not option.interface:
        parser.error("\n[-] Please specify the interface, use --help for more info")
    elif not option.new_MAC:
        parser.error("\n[-] Please specify the new_MAC address, use --help for more info")
    return option


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call("ifconfig " + interface + " down", shell=True)
    subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
    subprocess.call("ifconfig " + interface + " up", shell=True)


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not find MAC_address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC address: " + str(current_mac))
change_mac(interface=options.interface, new_mac=options.new_MAC)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_MAC:
    print("[+] New MAC address changed successfully")
else:
    print("[-] MAC address not changed")
