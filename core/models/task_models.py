from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class TaskProof(models.Model):
    task = models.ForeignKey("core.ServiceRequest", on_delete=models.CASCADE,related_name="proofs")
    worker = models.ForeignKey(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="task_proofs/",blank=True,null=True)
    note = models.TextField(blank=True,null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TaskHistory(models.Model):
    task = models.ForeignKey("core.ServiceRequest",on_delete=models.CASCADE,related_name="history")
    status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    