from django.urls import path
from .views import dashboard,BranchCreateView,BranchListView,BranchUpdateView,BranchDeleteView,SpecializationListView,SpecializationCreateView,SpecializationUpdateView,SpecializationDeleteView,DoctorCreateView,DoctorListView,DoctorUpdateView,DoctorDeleteView



app_name= 'administrator'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('branches/', BranchListView.as_view(), name='branch-list'),
    path('branches/create/', BranchCreateView.as_view(), name='branch-create'),
    path('branches/<int:pk>/update/', BranchUpdateView.as_view(), name='branch-update'),
    path('branches/<int:pk>/delete/', BranchDeleteView.as_view(), name='branch-delete'),
    path('specializations/', SpecializationListView.as_view(), name='specialization-list'),
    path('specializations/create/', SpecializationCreateView.as_view(), name='specialization-create'),
    path('specializations/<int:pk>/update/',SpecializationUpdateView.as_view(),name='specialization-update'),
    path('specializations/<int:pk>/delete/',SpecializationDeleteView.as_view(),name='specialization-delete'),
    path( 'doctors/',DoctorListView.as_view(),name="doctor-list"),
    path('doctors/create/',DoctorCreateView.as_view(),name="doctor_create"),
    path('doctors/<int:pk>/update/',DoctorUpdateView.as_view(),name="doctor-update"),
    path('doctors/<int:pk>/delete/',DoctorDeleteView.as_view(),name="doctor-delete"),

]