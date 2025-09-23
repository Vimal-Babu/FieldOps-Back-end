from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING","Pending"),
        ("ASSIGNED","Assigned"),
        ("COMPLETED","Completed"),
        ("CANCELLED","Cancelled"),
    ]

    URGENCY_CHOICES = [
        ("LOW","Low"),
        ("MEDIUM","Medium"),
        ("HIGH","High"),
    ]

    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="requests")
    title = models.CharField(max_length = 255 )
    description = models.TextField()
    location = models.CharField(max_length=255)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default="LOW")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,default="PENDING")
    assigned_worker = models.ForeignKey(
        User,on_delete=models.SET_NULL,null=True,blank=True,related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"