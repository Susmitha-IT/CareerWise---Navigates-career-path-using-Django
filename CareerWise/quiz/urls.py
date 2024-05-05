# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('st/', views.startquiz, name='startquiz'),
    path('quizstart/', views.quiz_view, name='quiz'),
    path('quiz-data/', views.quiz_data, name='quiz-data'),
]
