from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from .views import index, home, user_logout, login, signup

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('home/', home, name='home'),
    path('logout/', user_logout, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
