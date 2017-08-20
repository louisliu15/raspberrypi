from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm
from .models import Ruser, Device
from .functions import send_message_by_socket, recv_file, send_file ,recv_file_list


# Create your views here.
# send and receive message with device
def home(request):
    return render(request, 'web_server/home.html')


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
                    form = LoginForm()
                    return render(request, 'web_server/login.html',
                                  {'form': form, 'error': True, 'error_message': 'Your account is disabled.'})
            else:
                form = LoginForm()
                return render(request, 'web_server/login.html',
                              {'form': form, 'error': True, 'error_message': 'Invalid username/password!'})
    else:
        form = LoginForm()
        return render(request, 'web_server/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('web:home')))


@login_required
def show_device(request, user_id):
    try:
        device_list = Ruser.objects.get(pk=user_id).device.all()
        return render(request, 'web_server/device.html', {'devices': device_list})
    except:
        return render(request, 'web_server/device.html', {'error': True})


@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        dev_names = request.POST.getlist('devices[]')
        message = request.POST.get('message')
        return_message = ""
        # TODO validate if the user has the access to the device
        for dev_name in dev_names:
            return_message += dev_name + ": " + str(send_message_by_socket(dev_name, message)) + "\n"

        return_json = {'result': return_message}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    else:
        try:
            device_list = Ruser.objects.get(pk=user_id).device.all()
            return render(request, 'web_server/message.html', {'devices': device_list})
        except:
            return render(request, 'web_server/message.html', {'error': True})


@login_required
def file_upload(request, user_id):
    if request.method == 'POST':
        dev_name = request.POST.get('devices')
        file_name = request.FILES.get('file')

        # TODO validate if the user has the access to the device
        return_message = send_file(dev_name, file_name)

        return_json = {'result': return_message}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    else:
        try:
            device_list = Ruser.objects.get(pk=user_id).device.all()
            return render(request, 'web_server/file_upload.html', {'devices': device_list})
        except Exception as e:
            print(str(e))
            return render(request, 'web_server/file_upload.html', {'error': True})


@login_required
def file_download(request, user_id):
    if request.method == 'POST':
        dev_name = request.POST.get('devices')
        file_name = request.POST.get('file')
        if dev_name == None or file_name == None :
            return_json = {'error': True, 'error_msg': "Please select device or file name."}
            return HttpResponse(json.dumps(return_json), content_type='application/json')

        # TODO validate if the user has the access to the device
        # return_data is a boolean value, indecates if the file download is succeed or not
        return_data = recv_file(dev_name, file_name)

        return_json = {'result': return_data}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    else:
        try:
            device_list = Ruser.objects.get(pk=user_id).device.all()
            file_list = recv_file_list(device_list[0].name)
            return render(request, 'web_server/file_download.html', {'devices': device_list, "file_list": file_list})
        except Exception as e:
            print(e)
            return render(request, 'web_server/file_download.html', {'error': True, 'error_msg': "You didn't bind any device yet."})

@login_required
def get_file_list(request, user_id):
    if request.method == 'POST':
        dev_name = request.POST.get('devices')

        # TODO validate if the user has the access to the device

        return_message = recv_file_list(dev_name)
        return_json = {'result': return_message}
        return HttpResponse(json.dumps(return_json), content_type='application/json')
    else:
        try:
            device_list = Ruser.objects.get(pk=user_id).device.all()
            return render(request, 'web_server/file_upload.html', {'devices': device_list})
        except Exception as e:
            print(str(e))
            return render(request, 'web_server/file_upload.html', {'error': True})