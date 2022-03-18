from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=30)
    email         = models.EmailField(unique=True, max_length=245)
    password      = models.CharField(max_length=100)
    phone         = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    created_at    = models.DateTimeField(auto_now_add=True)  
    updated_at     = models.DateTimeField(auto_now= True)
    
    class Meta:
        db_table = "users"