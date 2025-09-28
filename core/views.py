from django.shortcuts import render
from rest_framework import generics,serializers,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models.user_models import CustomUser
from .models.service_models import ServiceRequest
from core.serializers import UserSerializer,ServiceRequestSerializer

class UserListCerateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.AllowAny]