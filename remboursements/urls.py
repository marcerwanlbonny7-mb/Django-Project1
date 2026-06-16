from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaiementCreateView.as_view(), name='paiement-create'),
    path('echeances/', views.EcheanceListView.as_view(), name='echeance-list'),
    path('historique/', views.HistoriquePaiementView.as_view(), name='paiement-historique'),
]
