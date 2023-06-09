"""sirest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trigger_2/', include('trigger_2.urls')),
    path('trigger_3/', include('trigger_3.urls')),
    path('trigger-5/', include('trigger_5.urls')),
    path('trigger_6/', include('trigger_6.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('trigger-4/', include('trigger_4.urls')),
    path('login_page/', include('login_page.urls')),
]
