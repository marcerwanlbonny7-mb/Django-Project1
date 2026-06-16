from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/lire/', views.NotificationLireView.as_view(), name='notification-lire'),
    path('lire-tout/', views.NotificationLireToutView.as_view(), name='notification-lire-tout'),
]
