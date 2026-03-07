from django.urls import path
from .views import home,specialization_detail,specialization_list






app_name= 'userapp'




urlpatterns = [
    path('', home, name='home'),
    path("specializations/",specialization_list,name="specialization_list"),
    path("specializations/<slug:slug>/",specialization_detail, name="specialization_detail"),
]