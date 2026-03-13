from django.urls import path
from .views import home,about,contact,specialization_detail,specialization_list,blog_list,blog_detail,doctor_list,doctor_detail,package_detail,package_list,insurance_detail,insurance_list,articles_detail,articles_list






app_name= 'userapp'




urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about-us'),
    path('contact/', contact, name='contact-us'),
    path("blogs/",blog_list,name="blog_list"),
    path("blogs/detail/",blog_detail, name="blog_detail"),
    path("specializations/",specialization_list,name="specialization_list"),
    path("specializations/<slug:slug>/",specialization_detail, name="specialization_detail"),
    path("doctors/",doctor_list,name="doctor_list"),
    path("doctors/<slug:slug>/",doctor_detail, name="doctor_detail"),
    path("packages/",package_list,name="packages_list"),
    path("packages/detail/",package_detail, name="packages_detail"),
    path("insurance/",insurance_list,name="insurance_list"),
    path("insurance/detail/",insurance_detail, name="insurance_detail"),
    path("articles/",articles_list,name="articles_list"),
    path("articles/detail/",articles_detail, name="articles_detail"),
]