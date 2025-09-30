from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models.user_models import CustomUser, UserRole
from .models.service_models import ServiceRequest
from .models.task_models import TaskProof, TaskHistory
from .serializers import (
    UserSerializer,
    ServiceRequestSerializer,
    TaskProofSerializer,
    TaskHistorySerializer
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary(request):
    print("dashbord view works")
    user = request.user
    data = {}

    if user.role == UserRole.ADMIN:
        data['total_users'] = CustomUser.objects.count()
        data['total_workers'] = CustomUser.objects.filter(role=UserRole.WORKER).count()
        data['total_customers'] = CustomUser.objects.filter(role=UserRole.USER).count()
        data['total_requests'] = ServiceRequest.objects.count()
        data['pending_requests'] = ServiceRequest.objects.filter(status="PENDING").count()
        data['completed_requests'] = ServiceRequest.objects.filter(status="COMPLETED").count()
    elif user.role == UserRole.WORKER:
        assigned = ServiceRequest.objects.filter(assigned_worker=user)
        data['assigned_requests'] = assigned.count()
        data['completed_requests'] = assigned.filter(status="COMPLETED").count()
    else: 
        customer_requests = ServiceRequest.objects.filter(customer=user)
        data['total_requests'] = customer_requests.count()
        data['pending_requests'] = customer_requests.filter(status="PENDING").count()
        data['completed_requests'] = customer_requests.filter(status="COMPLETED").count()

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_request(request, pk):
    try:
        service = ServiceRequest.objects.get(pk=pk)
    except ServiceRequest.DoesNotExist:
        return Response({"detail": "Service request not found."}, status=status.HTTP_404_NOT_FOUND)
    
    worker_id = request.data.get("worker_id")
    try:
        worker = CustomUser.objects.get(pk=worker_id, role=UserRole.WORKER)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Worker not found."}, status=status.HTTP_404_NOT_FOUND)

    service.assigned_worker = worker
    service.status = "ASSIGNED"
    service.save()
    return Response({"detail": f"Service request assigned to {worker.username}"})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_task(request, pk):
    try:
        service = ServiceRequest.objects.get(pk=pk)
    except ServiceRequest.DoesNotExist:
        return Response({"detail": "Service request not found."}, status=status.HTTP_404_NOT_FOUND)
    
    worker = request.user
    if service.assigned_worker != worker:
        return Response({"detail": "You are not assigned to this task."}, status=status.HTTP_403_FORBIDDEN)


    service.status = "IN_PROGRESS"
    service.save()

    TaskHistory.objects.create(
        task=service,
        status="IN_PROGRESS",
        changed_by=worker
    )

    return Response({"detail": f"Task {service.id} started by {worker.username}"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        user = self.get_object()
        if user.role != UserRole.WORKER:
            return Response({"detail": "Only workers can be approved."}, status=status.HTTP_400_BAD_REQUEST)
        user.is_approved = True
        user.save()
        return Response({"detail": f"{user.username} approved successfully."})


# --------- User Views ---------
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# --------- Service Request Views ---------
class ServiceRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.ADMIN:
            return ServiceRequest.objects.all()
        elif user.role == UserRole.WORKER:
            return ServiceRequest.objects.filter(assigned_worker=user)
        else:  
            return ServiceRequest.objects.filter(customer=user)

    def perform_create(self, serializer):

        if self.request.user.role != UserRole.USER:
            raise PermissionDenied("Only customers can create service requests.")
        serializer.save(customer=self.request.user)


class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


# --------- Task History Views ---------
class TaskHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.ADMIN:
            return TaskHistory.objects.all()
        elif user.role == UserRole.WORKER:
            return TaskHistory.objects.filter(changed_by=user)
        else:
            return TaskHistory.objects.filter(task__customer=user)

    def perform_create(self, serializer):
        serializer.save(changed_by=self.request.user)


# --------- Task Proof Views ---------
class TaskProofListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskProofSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.ADMIN:
            return TaskProof.objects.all()
        elif user.role == UserRole.WORKER:
            return TaskProof.objects.filter(worker=user)
        else:
            return TaskProof.objects.filter(task__customer=user)

    def perform_create(self, serializer):
        if self.request.user.role != UserRole.WORKER:
            raise PermissionDenied("Only workers can upload proof.")
        serializer.save(worker=self.request.user)
