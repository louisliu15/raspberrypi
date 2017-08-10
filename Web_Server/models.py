from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.URLField()
    port = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('address', 'port')

class Ruser(User):
    device = models.ManyToManyField(Device)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Raspberry User"
        verbose_name_plural = "Raspberry Users"