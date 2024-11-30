"""
URL configuration for database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from users.admin_views import download_logs

urlpatterns = [
   path('u/a/', include('users.admin_urls')),
   path('u/api/', include('users.urls')),
   path('p/api/', include('projects.urls')),
   path('c/api/', include('contractors.urls')),
   path('c/api/', include('contractors.urls')),
   path('files/upload/', TemplateView.as_view(template_name='bajenchik.html'), name='file-upload'),
   path('', download_logs ),
]
