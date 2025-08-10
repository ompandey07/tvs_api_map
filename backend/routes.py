from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    LoginAPIView, LogoutAPIView, DashboardAPIView,
    BlogViewSet, MailViewSet, CustomerSMSAPIView,
    DocumentationAPIView, health_check
)

# ======================================================================
# DRF ROUTER CONFIGURATION
# ======================================================================

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'mails', MailViewSet, basename='mail')

# ======================================================================
# API URL PATTERNS
# ======================================================================

urlpatterns = [
    # Health Check
    path('health/', health_check, name='api_health_check'),
    
    # Authentication
    path('auth/login/', LoginAPIView.as_view(), name='api_login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # Dashboard
    path('dashboard/', DashboardAPIView.as_view(), name='api_dashboard'),
    
    # Customer Management
    path('customers/', CustomerSMSAPIView.as_view(), name='api_customers'),
    
    # Documentation
    path('documentation/', DocumentationAPIView.as_view(), name='api_documentation'),
    
    # Router URLs (blogs, mails)
    path('', include(router.urls)),
    
    # DRF Browsable API
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)