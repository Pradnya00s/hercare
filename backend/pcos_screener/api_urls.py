from django.urls import path
from .api_views import pcos_form_predict_api, ultrasound_prediction_api, combined_prediction_api

urlpatterns = [
    path("pcos/form-predict/", pcos_form_predict_api),
    path("ultrasound/", ultrasound_prediction_api),
    path("combined-prediction/", combined_prediction_api),
]
