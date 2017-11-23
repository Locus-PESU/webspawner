from django.db import models
from django.contrib.auth.models import User


class RootProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(null=True)
    quote = models.CharField(max_length=140, default='')

    def __str__(self):
        return self.user.username
