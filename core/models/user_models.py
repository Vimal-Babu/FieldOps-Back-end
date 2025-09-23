from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    ADMIN = "ADMIN","Admin"
    WORKER = "WORKER","Field Worker"
    USER = "USER" ,"Customer"

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices= UserRole.choices,default=UserRole.USER)
    phone_number = models.CharField(max_length=15, blank=True,null=True)
    photo = models.ImageField(upload_to="Profiles/", blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    