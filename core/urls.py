from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,ServiceRequestListCreateView,ServiceRequestDetailView,TaskHistoryListCreateView, TaskProofListCreateView,dashboard_summary,assign_request,start_task

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('service-requests/', views.ServiceRequestListCreateView.as_view(), name='service-request-list-create'),
    path('service-requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service-request-detail'),
    path('service-requests/<int:pk>/start/', views.start_task, name='start-task'),
    path('task-history/', views.TaskHistoryListCreateView.as_view(), name='task-history-list-create'),
    path('service-requests/<int:pk>/assign/', assign_request, name='assign-service-request'),
    path('task-proof/', views.TaskProofListCreateView.as_view(), name='task-proof-list-create'),
    path('dashboard/', dashboard_summary, name='dashboard-summary'),

]
