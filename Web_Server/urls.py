from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sendMsg', views.sendMessage, name="sendMsg"),
]