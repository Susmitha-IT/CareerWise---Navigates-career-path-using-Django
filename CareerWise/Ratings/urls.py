from django.urls import path
from . import views

urlpatterns = [
    path('rating/', views.rating, name='rating'),
    path('rate/', views.rate, name='rate'),
    path('viewrating/', views.viewrating, name='viewrating'),
]
