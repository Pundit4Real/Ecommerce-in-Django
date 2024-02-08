from django.contrib.auth.models import User
from django.db import models

class customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Other fields and methods for your model...
