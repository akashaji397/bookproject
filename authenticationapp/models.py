from django.db import models
from django.contrib.auth.models import User
from django.db import models


    # Add any other fields you need

class UserProfile(models.Model):
    username=models.CharField(max_length=200)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password1=models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)
    
class loginTable(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password1=models.CharField(max_length=200)
    type=models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)

