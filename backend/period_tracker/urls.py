from django.urls import path
from .views import add_cycle, get_history, get_prediction, get_insights, get_phase, get_irregularity_analysis
from .views import delete_log


urlpatterns = [
    path("add/", add_cycle),
    path("history/", get_history),
    path("prediction/", get_prediction),
    path("insights/", get_insights),
    path('phase/', get_phase),
    path('irregularity/', get_irregularity_analysis),
    path('delete/<int:id>/', delete_log),
]