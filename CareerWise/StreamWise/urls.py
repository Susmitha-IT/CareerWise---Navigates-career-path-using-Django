from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start, name='streamwise_start'),
    path('questionnaire/', views.questionnaire_view, name='questionnaire'),
    path('predict_stream/', views.predict_stream, name='predict_stream'),
    path('result/<str:recommended_stream>/', views.result, name='result'),
]
