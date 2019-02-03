from . import views
from django.urls import path



urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='user-register'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
]
