from django.db import models

class User(models.Model):
    name      = models.CharField(max_length=40)
    email     = models.EmailField(max_length=254)
    password  = models.CharField(max_length=50)
    phone     = models.IntegerField()
    
    class Meta:
        db_table = "users"