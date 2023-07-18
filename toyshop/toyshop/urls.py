"""
URL configuration for toyshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from toys import views

urlpatterns = [
   path('', views.home, name='home'),
   path('toys/', views.toy_list, name='toy_list'),
   path('toys/<int:toy_id>/', views.toy_detail, name='toy_detail'),
   path('contact/', views.contact, name='contact'),
   path('about/', views.about, name='about'),
   path("admin/", admin.site.urls),
]
