from django.urls import path
from . import views

urlpatterns = [
    path('', views.DemandeCreditListCreateView.as_view(), name='credit-list'),
    path('<int:pk>/', views.DemandeCreditDetailView.as_view(), name='credit-detail'),
    path('<int:pk>/statut/', views.DemandeCreditStatutUpdateView.as_view(), name='credit-statut'),
    path('<int:pk>/echeancier/', views.EcheancierView.as_view(), name='credit-echeancier'),
]
