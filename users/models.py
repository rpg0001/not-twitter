from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="")
    date_joined = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username
