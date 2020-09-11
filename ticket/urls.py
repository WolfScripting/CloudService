from django.urls import path
from ticket import views

urlpatterns = [
    path('v1/generate/', views.generate),
    path('v1/validate/', views.validate),
]