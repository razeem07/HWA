from django.urls import path
from .views import admin_login,user_logout,user_register,user_login


app_name= 'accounts'

urlpatterns = [

    path('admin-login/', admin_login, name='admin-login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
]