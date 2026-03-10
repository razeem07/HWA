from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.utils.decorators import method_decorator
from django.contrib import messages
from .decorators import admin_required
from .models import Branch,Specialization,Doctor
from .forms import BranchForm,SpecializationForm,DoctorForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse

User = get_user_model()



# Create your views here.
@admin_required
def dashboard(request):
    return render(request, 'administrator/dashboard.html')


@method_decorator(admin_required, name='dispatch')
class BranchCreateView(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'administrator/branches/branch.html'
    success_url = reverse_lazy('administrator:dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Branch created successfully")
        return super().form_valid(form)

  

@method_decorator(admin_required, name='dispatch')
class BranchListView(ListView):
    model = Branch
    template_name = 'administrator/branches/list.html'
    ordering = ['-created_at']


@method_decorator(admin_required, name='dispatch')
class BranchUpdateView(UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'administrator/branches/branch.html'
    success_url = reverse_lazy('administrator:branch-list')

    def form_valid(self, form):
        messages.success(self.request, "Branch updated successfully")
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class BranchDeleteView(DeleteView):
    model = Branch
    template_name = 'administrator/branches/confirm_delete.html'
    success_url = reverse_lazy('administrator:branch-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Branch deleted successfully")
        return super().delete(request, *args, **kwargs)
    


@method_decorator(admin_required, name='dispatch')
class SpecializationCreateView(CreateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'administrator/specialization/specialization.html'
    success_url = reverse_lazy('administrator:specialization-list')

    def form_valid(self, form):
        messages.success(self.request, "Specialization created successfully")
        return super().form_valid(form)
    
@method_decorator(admin_required, name='dispatch')
class SpecializationListView(ListView):
    model = Specialization
    template_name = 'administrator/specialization/list.html'
    ordering = ['-created_at']


@method_decorator(admin_required, name='dispatch')
class SpecializationUpdateView(UpdateView):
    model = Specialization
    form_class = SpecializationForm
    template_name = 'administrator/specialization/specialization.html'
    success_url = reverse_lazy('administrator:specialization-list')

    def form_valid(self, form):
        messages.success(self.request, "Specialization updated successfully")
        return super().form_valid(form)
    
@method_decorator(admin_required, name='dispatch')
class SpecializationDeleteView(DeleteView):
    model = Specialization
    template_name = 'administrator/specialization/confirm_delete.html'
    success_url = reverse_lazy('administrator:specialization-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Specialization deleted successfully")
        return super().delete(request, *args, **kwargs)
    



class DoctorCreateView(CreateView):

    model = Doctor
    form_class = DoctorForm
    template_name = "administrator/doctor/doctor.html"
    success_url = reverse_lazy("administrator:doctor-list")

    @transaction.atomic
    def form_valid(self, form):

        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            phone_number=form.cleaned_data["phone_number"],
            password="doctor123"
        )

        user.is_doctor = True
        user.save()

        doctor = form.save(commit=False)
        doctor.user = user
        doctor.save()

        return super().form_valid(form)
    

@method_decorator(admin_required, name='dispatch')
class DoctorListView(ListView):
    model = Doctor
    context_object_name = "doctors"
    template_name = 'administrator/doctor/list.html'
    ordering = ['-created_at']


@method_decorator(admin_required, name='dispatch')
class DoctorUpdateView(UpdateView):

    model = Doctor
    form_class = DoctorForm
    template_name = "administrator/doctor/doctor.html"
    success_url = reverse_lazy("administrator:doctor-list")


    def get_initial(self):

        initial = super().get_initial()

        doctor = self.get_object()
        user = doctor.user

        initial["username"] = user.username
        initial["email"] = user.email
        initial["first_name"] = user.first_name
        initial["last_name"] = user.last_name
        initial["phone_number"] = user.phone_number

        return initial

    def form_valid(self, form):

        doctor = form.save(commit=False)
        user = doctor.user

        user.username = form.cleaned_data["username"]
        user.email = form.cleaned_data["email"]
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.phone_number = form.cleaned_data["phone_number"]

        user.save()
        doctor.save()

        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class DoctorDeleteView(DeleteView):

    model = Doctor
    template_name = "administrator/doctor/confirm_delete.html"
    success_url = reverse_lazy("administrator:doctor-list")





def load_specializations(request):

    branch_id = request.GET.get("branch")

    specializations = Specialization.objects.filter(
        branch_id=branch_id
    ).values("id", "name")

    return JsonResponse(list(specializations), safe=False)