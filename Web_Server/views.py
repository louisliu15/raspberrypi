from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import socket, os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from Web_Server.forms import LoginForm, RegisterForm


# Create your views here.
# send and receive message with device
def home(request):
    return render(request, 'web_server/home.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('web:home'))
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login information.')
    else:
        form = LoginForm()
        return render(request, 'web_server/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('web:home')))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('web:login'))
        else:
            # print(form.errors)
            error = form.errors
            form = RegisterForm()
            return render(request, 'web_server/register.html', {'form': form, 'error': error})
    else:
        form = RegisterForm()
        return render(request, 'web_server/register.html', {'form': form})


def send_message(request):
    response = HttpResponse()
    conn = socket.socket()
    conn.connect(("10.204.46.92", 8000))
    # establish connection
    conn.sendall(bytes("M", encoding="utf-8"))
    recv_bytes = conn.recv(1024)
    print(str(recv_bytes, encoding="utf-8"))
    # send and receive message
    conn.sendall(bytes("This is web server.", encoding="utf-8"))
    recv_bytes = conn.recv(1024)
    recv_str = str(recv_bytes, encoding="utf-8")

    response.write(recv_str)
    return response


# receive file from device
def recv_file(request):
    response = HttpResponse()
    conn = socket.socket()
    conn.connect(("10.204.46.92", 8000))
    conn.sendall(bytes("D", encoding="utf-8"))

    # get file name and file size from remote host
    recv_bytes = conn.recv(1024)
    file_info = str(recv_bytes, encoding="utf-8")

    file = file_info.split('|')
    file_name = file[0]
    file_size = int(file[1])

    conn.sendall(bytes("start transfer", encoding="utf-8"))
    has_size = 0
    f = open(file_name, "wb")
    while True:
        if file_size == has_size:
            break
        data = conn.recv(1024)
        f.write(data)
        has_size += len(data)

    f.close()
    conn.close()
    response.write("File transfer succeed.")
    return response


def send_file(request):
    response = HttpResponse()
    conn = socket.socket()
    conn.connect(("10.204.46.92", 8000))
    conn.sendall(bytes("U", encoding="utf-8"))
    # wait for device answer
    recv_bytes = conn.recv(1024)
    print(str(recv_bytes, encoding="utf-8"))
    # send file name
    conn.sendall(bytes("test1.png", encoding="utf-8"))
    recv_bytes = conn.recv(1024)
    print(str(recv_bytes, encoding="utf-8"))
    # send file size
    fsize = os.stat("test1.png").st_size
    conn.sendall(bytes(str(fsize), encoding="utf-8"))
    recv_bytes = conn.recv(1024)
    print(str(recv_bytes, encoding="utf-8"))

    # start file transfer
    with open("test1.png", "rb") as f:
        for line in f:
            conn.sendall(line)

    f.close()
    conn.close()
    response.write("File transfer succeed.")
    return response
