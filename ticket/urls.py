from django.urls import path
from ticket import views

urlpatterns = [
    path('generate/', views.generate),
    path('validate/', views.validate),
]