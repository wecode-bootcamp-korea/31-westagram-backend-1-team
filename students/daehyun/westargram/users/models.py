from enum import unique
from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=30)
    email        = models.CharField(max_length=30, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=25)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'