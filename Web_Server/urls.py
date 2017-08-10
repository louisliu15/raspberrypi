from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home', views.home, name='home'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^register', views.register, name='register'),
    url(r'^message', views.send_message, name="sendMsg"),
    url(r'^download', views.recv_file, name="recvFile"),
    url(r'^upload', views.send_file, name="sendFile"),
]