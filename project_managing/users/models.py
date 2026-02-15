
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    about_me = models.TextField(blank=True, null=True)
