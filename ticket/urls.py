from django.urls import path
from ticket import views

urlpatterns = [
    path('ticket/validate', views.validate)
]