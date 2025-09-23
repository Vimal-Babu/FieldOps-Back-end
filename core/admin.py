from django.contrib import admin
from .models.user_models import CustomUser
from .models.service_models import ServiceRequest
from .models.task_models import TaskHistory,TaskProof


# Register your models here.

admin.site.register(CustomUser)
#admin.site.register(ServiceRequest)
admin.site.register(TaskHistory)
admin.site.register(TaskProof)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "customer", "assigned_worker", "status", "urgency", "created_at")
    list_filter = ("status", "urgency", "created_at")
    search_fields = ("title", "description", "customer__email", "assigned_worker__email")
    ordering = ("-created_at",)
