from rest_framework import serializers
from .models.user_models import CustomUser
from .models.service_models import ServiceRequest
from .models.task_models import TaskProof, TaskHistory

# --------- User Serializer ---------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

# --------- Service Request Serializer ---------
class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    assigned_worker = UserSerializer(read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = "__all__"

# --------- Task History Serializer ---------
class TaskHistorySerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskHistory
        fields = "__all__"

# --------- Task Proof Serializer ---------
class TaskProofSerializer(serializers.ModelSerializer):
    worker = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskProof
        fields = "__all__"
