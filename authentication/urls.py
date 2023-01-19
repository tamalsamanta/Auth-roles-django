from django.contrib import admin
from django.urls import path
from .views import ResetPasswordView
from .views import *

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user_home/', user_home, name='user_home'),
    path('admin_home/', admin_home, name='admin_home'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
]
