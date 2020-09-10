from django.urls import path
from ticket import views

urlpatterns = [
    path('validate/', views.validate),
    path('generate/', views.generate)
]