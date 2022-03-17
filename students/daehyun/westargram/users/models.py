from django.db import models

class User(models.Model):
    name        = models.CharField(max_length=30)
    email       = models.CharField(max_length=30)
    password    = models.CharField(max_length=30)
    phonenumber = models.PhoneNumberField((""))
    
    class Meta:
        db_table = 'users'