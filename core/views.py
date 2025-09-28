from rest_framework import generics, permissions
from .models.user_models import CustomUser
from .models.service_models import ServiceRequest
from .models.task_models import TaskProof, TaskHistory
from .serializers import UserSerializer, ServiceRequestSerializer, TaskProofSerializer, TaskHistorySerializer

# --------- Users ---------
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# --------- Service Requests ---------
class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

# --------- Task History ---------
class TaskHistoryListCreateView(generics.ListCreateAPIView):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

# --------- Task Proof ---------
class TaskProofListCreateView(generics.ListCreateAPIView):
    queryset = TaskProof.objects.all()
    serializer_class = TaskProofSerializer
    permission_classes = [permissions.IsAuthenticated]
