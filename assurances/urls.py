from django.urls import path
from . import views

urlpatterns = [
    path('formules/', views.FormuleAssuranceListView.as_view(), name='formule-list'),
    path('souscrire/', views.SouscriptionCreateView.as_view(), name='souscription-create'),
    path('mes-polices/', views.MesPolicesView.as_view(), name='mes-polices'),
    path('<int:pk>/resilier/', views.ResilierSouscriptionView.as_view(), name='souscription-resilier'),
]
