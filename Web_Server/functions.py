import socket, os

from .models import Device

def send_message_by_socket(dev, message):
    device = Device.objects.get(name=dev)
    try:
        conn = socket.socket()
        conn.connect((device.address, device.port))
        # conn.connect((device.address, device.port))
        # establish connection
        conn.sendall(bytes("M", encoding="utf-8"))
        recv_bytes = conn.recv(1024)
        print(str(recv_bytes, encoding="utf-8"))
        # # send and receive message
        return str(recv_bytes, encoding="utf-8")
    except:
        return "Can not connect to device."

# receive file from device
def recv_file(dev, file_name):
    device = Device.objects.get(name=dev)
    try:
        conn = socket.socket()
        conn.connect((device.address, device.port))
        conn.sendall(bytes("D", encoding="utf-8"))

        # send file name
        recv_bytes = conn.recv(1024)
        conn.sendall(bytes(file_name, encoding="utf-8"))
        # get file size from remote device
        recv_bytes = conn.recv(1024)
        file_size = int(str(recv_bytes, encoding="utf-8"))
        # set local storage path
        base_path = "Web_Server/static/download/" + file_name
        # call remote device to start file transmission
        conn.sendall(bytes("start transfer", encoding="utf-8"))
        has_size = 0
        f = open(base_path, "wb")
        while True:
            if file_size == has_size:
                break
            data = conn.recv(1024)
            f.write(data)
            has_size += len(data)

        f.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

# send file to remote device
def send_file(dev, file):
    device = Device.objects.get(name=dev)
    try:
        conn = socket.socket()
        conn.connect((device.address, device.port))
        conn.sendall(bytes("U", encoding="utf-8"))
        # wait for device answer
        recv_bytes = conn.recv(1024)
        print(str(recv_bytes, encoding="utf-8"))
        # send file name
        conn.sendall(bytes(file.name, encoding="utf-8"))
        recv_bytes = conn.recv(1024)
        print(str(recv_bytes, encoding="utf-8"))
        # send file size
        conn.sendall(bytes(str(file.size), encoding="utf-8"))
        recv_bytes = conn.recv(1024)
        print(str(recv_bytes, encoding="utf-8"))
        # upload user's file to the device
        for line in file:
            conn.sendall(line)

        # # send file on local server
        # # send file size
        # # fsize = os.stat("test1.png").st_size
        # recv_bytes = conn.recv(1024)
        # print(str(recv_bytes, encoding="utf-8"))
        #
        # # start file transfer
        # with open("test1.png", "rb") as f:
        #     for line in f:
        #         conn.sendall(line)
        # f.close()

        conn.close()
        return "File upload succeed"
    except Exception as e:
        print(e)
        return "File upload failed"

def recv_file_list(dev):
    device = Device.objects.get(name=dev)
    try:
        conn = socket.socket()
        conn.connect((device.address, device.port))
        conn.sendall(bytes("L", encoding="utf-8"))

        # receive file list
        recv_bytes = conn.recv(1024)
        if len(recv_bytes) == 0:
            return False
        file_list = str(recv_bytes, encoding="utf-8").split("$$")
        file_list.pop(-1)

        return file_list
    except Exception as e:
        print(e)
        return False