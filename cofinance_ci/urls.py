from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

auth_pages = login_required

urlpatterns = [
    path('', lambda request: redirect('static/frontend/index.html')),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('dashboard/', auth_pages(TemplateView.as_view(template_name='dashboard.html')), name='dashboard'),
    path('credits/', auth_pages(TemplateView.as_view(template_name='credits.html')), name='credits'),
    path('assurances/', auth_pages(TemplateView.as_view(template_name='assurances.html')), name='assurances'),
    path('chat/', auth_pages(TemplateView.as_view(template_name='chat.html')), name='chat'),
    path('notifications/', auth_pages(TemplateView.as_view(template_name='notifications.html')), name='notifications'),
    path('admin/stats/', auth_pages(TemplateView.as_view(template_name='admin_stats.html')), name='admin-stats'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/credits/', include('credits.urls')),
    path('api/remboursements/', include('remboursements.urls')),
    path('api/assurances/', include('assurances.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
