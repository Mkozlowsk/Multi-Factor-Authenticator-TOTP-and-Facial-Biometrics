"""
URL configuration for bemsi_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from authentication.views import register, login_view, verify_otp, show_qr_code, register_face, login_with_face

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('qr-code/<int:user_id>/', show_qr_code, name='show_qr_code'),
    path('register-face/<int:user_id>/', register_face, name='register_face'),
    path('login-with-face/', login_with_face, name='login_with_face'),
]