from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]
