from django.urls import path
from . import views

urlpatterns = [
    path('agents/', views.AgentListView.as_view(), name='agent-list'),
    path('conversations/', views.ConversationListCreateView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/messages/', views.MessageListView.as_view(), name='conversation-messages'),
    path('conversations/<int:pk>/assigner/', views.AssignerConversationView.as_view(), name='conversation-assigner'),
]
