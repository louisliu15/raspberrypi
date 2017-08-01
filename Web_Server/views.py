from django.shortcuts import render, get_object_or_404
import socket

# Create your views here.
def sendMessage(request):
    conn = socket.socket()
    code = conn.connect(("10.204.46.92", 8000))
    conn.sendall(bytes("remote request from client", encoding="utf-8"))
    recv_bytes = conn.recv(1024)
    recv_str = str(recv_bytes, encoding="utf-8")
    return recv_str