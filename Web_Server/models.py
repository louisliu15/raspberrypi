from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(User):
    address = models.URLField()

    def __str__(self):
        return self.username + " " + self.address