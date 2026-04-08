from django.urls import path
from .views import home,about,contact,specialization_detail,specialization_list,blog_list,blog_detail,doctor_list,doctor_detail,package_list,insurance_list,articles_detail,articles_list,contact_submit,service_detail,legal_page_detail,package_list_ajax,gallery_page,subscribe_newsletter






app_name= 'userapp'




urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about-us'),
    path('contact/', contact, name='contact-us'),
    path('contact/submit/', contact_submit, name='contact-submit'),
    path("blogs/",blog_list,name="blog_list"),
    path('blogs/<slug:slug>/',blog_detail, name='blog-detail'), 
    path("specializations/",specialization_list,name="specialization_list"),
    path("specializations/<slug:slug>/",specialization_detail, name="specialization_detail"),
    path('service/<slug:slug>/', service_detail, name='service_detail'),
    path("doctors/",doctor_list,name="doctor_list"),
    path("doctors/<slug:slug>/",doctor_detail, name="doctor_detail"),
    path("packages/",package_list,name="packages-list"),
    path('packages/ajax/', package_list_ajax, name='package_list_ajax'),
  
    path("insurance/",insurance_list,name="insurance_list"),
  
    path("articles/",articles_list,name="articles_list"),
    path("articles/<slug:slug>/",articles_detail, name="articles_detail"),
    path('legal/<slug:slug>/', legal_page_detail, name='legal-page'),
    path('gallery/', gallery_page, name='gallery_page'),
    path("subscribe/", subscribe_newsletter, name="subscribe_newsletter"),
]