from django.urls import path 
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.register, name='register'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name='logout'),
    path("home/", views.home, name='home'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("otp-verification/", views.otp_verification, name="otp_verification"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path('edit/<int:content_id>/', views.edit_content, name='edit_content'),
    path('edit/<int:content_id>/', views.edit_content, name='edit_content'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
