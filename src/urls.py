"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

admin_path = settings.ADMIN_PATH + "/"

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path(admin_path, admin.site.urls),
    path('health-check/', include('health_check.urls')),
    path('sentry-debug/', trigger_error),
    path('', include('social_django.urls', namespace='social')),
    
    path('v1/ticket/', include('ticket.urls')),
    path('', include('user.urls'))
]
