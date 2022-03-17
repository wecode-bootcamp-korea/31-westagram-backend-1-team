from turtle import update
from venv import create
from django.db import models


class User(models.Model):
    name          = models.CharField(max_length=30)
    email         = models.EmailField(unique=True, max_length=245)
    password      = models.CharField(max_length=100)
    phone         = models.CharField(max_length=100)
    date_of_birth = models.DateField(auto_now_add=False,auto_now=False)
    created_at    = models.DateField(auto_now_add=True, auto_now=False)  
    update_at     = models.DateField(auto_now_add=True, auto_now= False)
    
    class Meta:
        db_table = "users"