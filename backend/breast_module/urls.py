from django.urls import path
from .views import full_assessment

urlpatterns = [
    path('full-assessment/', full_assessment),
] 