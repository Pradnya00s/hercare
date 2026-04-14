from django.urls import path
from .views import (
    RegisterView,
    login_view,
    profile_view,
    profile_setup_view,
    period_tracker_log_view,
    period_tracker_history_view,
    chat_message_view,
    chat_history_view,
    breast_cancer_history_view,
    pcos_history_view,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    # This maps to /api/auth/profile/setup/ based on your project urls.py
    path('profile/setup/', profile_setup_view, name='profile-setup'),
    path('profile/', profile_view, name='profile'),
    path('profile/period-log/', period_tracker_log_view, name='period-log'),
    path('profile/period-history/', period_tracker_history_view, name='period-history'),
    path('profile/chat/', chat_history_view, name='chat-history'),
    path('profile/chat/send/', chat_message_view, name='chat-send'),
    path('profile/breast-cancer/', breast_cancer_history_view, name='breast-cancer-history'),
    path('profile/pcos-history/', pcos_history_view, name='pcos-history'),
]