from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username= models.CharField(max_length=100)
    bio = models.CharField(max_length=200,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to="profile-image",null=True,blank=True)
    full_name = models.CharField(max_length=200)
    bio = models.CharField(max_length=200, null=True,blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name