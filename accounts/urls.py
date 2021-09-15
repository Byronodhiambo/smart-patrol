
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('get_help', views.get_help, name='get_help'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout, name= "logout"),
    path("profile/", views.profile, name= "profile"),


]
