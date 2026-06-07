from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication endpoints
    path("api/auth/", include("accounts.urls", namespace="accounts")),


    # Dashboard endpoint
    path("api/dashboard/", include("dashboard.urls")),

    # Existing PCOS endpoints
    path("", include("pcos_screener.api_urls")),
    path("api/", include("pcos_screener.api_urls")),
    path('api/chat/', include('chatbot.urls')),
    path('api/breast/', include('breast_module.urls')),
    path("api/period/", include("period_tracker.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)