from django.db import models


class User(models.Model):
    name        = models.CharField(max_length=30)
    email       = models.EmailField(max_length=245)
    password    = models.CharField(max_length=100)
    phone       = models.IntegerField(max_length=120)

    class Meta:
        db_table : "users"