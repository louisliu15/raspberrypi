from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^device/(?P<user_id>\d+)$', views.show_device, name='device'),
    url(r'^message/(?P<user_id>\d+)$', views.send_message, name="send_msg"),
    url(r'^file/upload/(?P<user_id>\d+)$', views.file_upload, name="file_upload"),
    url(r'^file/download/(?P<user_id>\d+)$', views.file_download, name="file_download"),
    url(r'^file/list/(?P<user_id>\d+)$', views.get_file_list, name="file_list"),
]