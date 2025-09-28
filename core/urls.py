from django.urls import path
from . import views

urlpatterns = [
    # Users
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # Service Requests
    path('requests/', views.ServiceRequestListCreateView.as_view(), name='service-request-list-create'),
    path('requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service-request-detail'),

    # Task History
    path('tasks/history/', views.TaskHistoryListCreateView.as_view(), name='task-history-list-create'),

    # Task Proof
    path('tasks/proof/', views.TaskProofListCreateView.as_view(), name='task-proof-list-create'),
]
