from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterCreateView, ResendCodeView, VerifyView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterCreateView.as_view(template_name='users/register.html'), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('resend-code/', ResendCodeView.as_view(), name='resend_code'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
