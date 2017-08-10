from django.contrib import admin
from .models import Ruser, Device
# Register your models here.
admin.site.register(Ruser)

class DeviceAdmin(admin.ModelAdmin):
    list_display=('name','address', 'port')

admin.site.register(Device, DeviceAdmin)