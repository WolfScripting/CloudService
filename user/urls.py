from django.urls import path
from user import views

urlpatterns = [
    path('', views.home, name="home"),
    path('token/', views.token, name="token"),
]