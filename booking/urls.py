from django.urls import path
from .views import book_appointment,load_doctors,load_slots

app_name= 'booking'

urlpatterns = [
     path('book/', book_appointment, name='book_appointment'),
     path('load-doctors/', load_doctors, name='load_doctors'),
     path('load-slots/', load_slots, name='load_slots'),
]