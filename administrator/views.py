from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from django.utils.decorators import method_decorator
from django.contrib import messages
from .decorators import admin_required
from .models import Branch,Specialization,Doctor,ListingPage,Content,ContentCategory,Tag,AboutPage,Testimonial,TeamMember,ContactPage,Service,Packages,Insurance,LegalPage,GlobalSettings,SocialLink,MenuGroup,MenuItem,HomePage,DoctorSchedule,DoctorLeave,Gallery
from .forms import BranchForm,SpecializationForm,DoctorForm,ListingPageForm,ContentForm,ContentCategoryForm,AboutPageForm,EducationFormSet,CertificationFormSet,ExpertiseFormSet,MembershipFormSet,FAQFormSet,TestimonialForm,TeamMemberForm,ContactPageForm,ServiceForm,ServiceFAQFormSet,PackageCategoryForm,PackageFeatureFormSet,InsuranceForm,LegalPageForm,GlobalSettingsForm,SocialLinkForm,MenuGroupForm,MenuItemFormSet,HomePageForm,HomeBannerFormSet,HomeFeatureFormSet,WhyChooseFormSet,HomeFAQFormSet,HighlightFormSet,DoctorScheduleForm,DoctorScheduleTimeFormSet,DoctorLeaveForm,GalleryImage,GalleryForm
from userapp.models import ContactSubmission
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse
from booking.models import Appointment
from datetime import date
from utils.sendmessage import send_whatsapp_message




User = get_user_model()



# Create your views here.
@admin_required
def dashboard(request):


    today = date.today()

    bookings = Appointment.objects.filter(date=today)


    # 🔥 SUMMARY
    total = bookings.count()
    approved = bookings.filter(status="approved").count()
    pending = bookings.filter(status="pending").count()
    cancelled = bookings.filter(status="cancelled").count()

    # 🔥 TODAY LEAVES
    today_leaves = DoctorLeave.objects.filter(date=today).select_related("doctor")


    context = {
        "doctor_count": Doctor.objects.count(),
        "specialization_count": Specialization.objects.count(),
        "service_count": Service.objects.count(),
        "package_count": Packages.objects.count(),
        "total": total,
        "approved": approved,
        "pending": pending,
        "cancelled": cancelled,
        "today_leaves": today_leaves,
    }
    return render(request, 'administrator/dashboard.html',context)


def about_manage(request):

    about = AboutPage.objects.first()  # get existing (if any)

    if request.method == "POST":
        form = AboutPageForm(
            request.POST,
            request.FILES,
            instance=about
        )

        if form.is_valid():
            form.save()
             # 🔥 SUCCESS MESSAGE
            messages.success(request, "About page updated successfully!")
            return redirect('administrator:about-manage')

        else:
            print("FORM ERRORS ❌", form.errors)  # 🔥 ADD THIS


    else:
        form = AboutPageForm(instance=about)

    

    return render(
        request,
        "administrator/pages/about.html",
        {"form": form, "about": about}
    )

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


    # ✅ ADD FORMSETS TO CONTEXT
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            # context['service_formset'] = ServiceFormSet(self.request.POST, self.request.FILES)
            context['faq_formset'] = FAQFormSet(self.request.POST)
        else:
            # context['service_formset'] = ServiceFormSet()
            context['faq_formset'] = FAQFormSet()

        return context

    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()

        # service_formset = context['service_formset']
        faq_formset = context['faq_formset']

        # 🔥 VALIDATE ALL
        if not  faq_formset.is_valid():
            print("FORMSET ERRORS ❌")
            # print(service_formset.errors)
            print(faq_formset.errors)
            return self.form_invalid(form)

        specialization = form.save()

        # 🔥 SAVE SERVICES
        # service_formset.instance = specialization
        # service_formset.save()

        # 🔥 SAVE FAQ
        faq_formset.instance = specialization
        faq_formset.save()

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

        # ✅ ADD FORMSETS
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            # context['service_formset'] = ServiceFormSet(
            #     self.request.POST,
            #     self.request.FILES,
            #     instance=self.object
            # )
            context['faq_formset'] = FAQFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            # context['service_formset'] = ServiceFormSet(instance=self.object)
            context['faq_formset'] = FAQFormSet(instance=self.object)

        return context
    
    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()

        # service_formset = context['service_formset']
        faq_formset = context['faq_formset']

        if not faq_formset.is_valid():
            print("FORMSET ERRORS ❌")
            # print(service_formset.errors)
            print(faq_formset.errors)
            return self.form_invalid(form)

        specialization = form.save()

        # service_formset.instance = specialization
        # service_formset.save()

        faq_formset.instance = specialization
        faq_formset.save()
        
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
    


@method_decorator(admin_required, name='dispatch')
class ServiceCreateView(CreateView):

    model = Service
    form_class = ServiceForm
    template_name = "administrator/service/manage.html"
    success_url = reverse_lazy("administrator:service-list")

     # ✅ ADD FORMSET TO CONTEXT
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['faq_formset'] = ServiceFAQFormSet(self.request.POST)
        else:
            context['faq_formset'] = ServiceFAQFormSet()

        return context
    
    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()
        faq_formset = context['faq_formset']

        # 🔥 VALIDATE
        if not faq_formset.is_valid():
            print("FAQ FORMSET ERRORS ❌", faq_formset.errors)
            return self.form_invalid(form)

        # ✅ SAVE SERVICE
        service = form.save()

        # ✅ SAVE FAQ
        faq_formset.instance = service
        faq_formset.save()


        messages.success(self.request, "Service created successfully")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class ServiceUpdateView(UpdateView):

    model = Service
    form_class = ServiceForm
    template_name = "administrator/service/manage.html"
    success_url = reverse_lazy("administrator:service-list")

    # ✅ CONTEXT WITH EXISTING INSTANCE
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['faq_formset'] = ServiceFAQFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['faq_formset'] = ServiceFAQFormSet(
                instance=self.object
            )

        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        faq_formset = context['faq_formset']

        # 🔥 VALIDATE
        if not faq_formset.is_valid():
            print("FAQ FORMSET ERRORS ❌", faq_formset.errors)
            return self.form_invalid(form)

        # ✅ SAVE SERVICE
        service = form.save()

        # ✅ SAVE FAQ
        faq_formset.instance = service
        faq_formset.save()
        messages.success(self.request, "Service updated successfully")
        return super().form_valid(form)
    
class ServiceListView(ListView):
    model = Service
    template_name = "administrator/service/list.html"
    context_object_name = "services"

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'administrator/service/confirm_delete.html'
    success_url = reverse_lazy("administrator:service-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Service deleted successfully")
        return super().delete(request, *args, **kwargs)


@method_decorator(admin_required, name='dispatch')
class DoctorCreateView(CreateView):

    model = Doctor
    form_class = DoctorForm
    template_name = "administrator/doctor/doctor.html"
    success_url = reverse_lazy("administrator:doctor-list")

   # ✅ STEP 1: Add ALL formsets
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['edu_formset'] = EducationFormSet(self.request.POST)
            context['cert_formset'] = CertificationFormSet(self.request.POST)
            context['exp_formset'] = ExpertiseFormSet(self.request.POST)
            context['mem_formset'] = MembershipFormSet(self.request.POST)
        else:
            context['edu_formset'] = EducationFormSet()
            context['cert_formset'] = CertificationFormSet()
            context['exp_formset'] = ExpertiseFormSet()
            context['mem_formset'] = MembershipFormSet()

        return context

    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()
        edu_formset = context['edu_formset']
        cert_formset = context['cert_formset']
        exp_formset = context['exp_formset']
        mem_formset = context['mem_formset']

         # ✅ VALIDATE ALL
        if not (
            edu_formset.is_valid() and
            cert_formset.is_valid() and
            exp_formset.is_valid() and
            mem_formset.is_valid()
        ):
            print("FORMSET ERRORS ❌")
            print(edu_formset.errors)
            print(cert_formset.errors)
            print(exp_formset.errors)
            print(mem_formset.errors)
            return self.form_invalid(form)

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


        # 🔥 Save education formset
        edu_formset.instance = doctor
        edu_formset.save()

        cert_formset.instance = doctor
        cert_formset.save()

        exp_formset.instance = doctor
        exp_formset.save()

        mem_formset.instance = doctor
        mem_formset.save()

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
    
     
    # ✅ ADD ALL FORMSETS
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['edu_formset'] = EducationFormSet(self.request.POST, instance=self.object)
            context['cert_formset'] = CertificationFormSet(self.request.POST, instance=self.object)
            context['exp_formset'] = ExpertiseFormSet(self.request.POST, instance=self.object)
            context['mem_formset'] = MembershipFormSet(self.request.POST, instance=self.object)
        else:
            context['edu_formset'] = EducationFormSet(instance=self.object)
            context['cert_formset'] = CertificationFormSet(instance=self.object)
            context['exp_formset'] = ExpertiseFormSet(instance=self.object)
            context['mem_formset'] = MembershipFormSet(instance=self.object)

        return context
    
    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()
        edu_formset = context['edu_formset']
        cert_formset = context['cert_formset']
        exp_formset = context['exp_formset']
        mem_formset = context['mem_formset']

         # ✅ VALIDATE ALL
        if not (
            edu_formset.is_valid() and
            cert_formset.is_valid() and
            exp_formset.is_valid() and
            mem_formset.is_valid()
        ):
            print("FORMSET ERRORS ❌")
            print(edu_formset.errors)
            print(cert_formset.errors)
            print(exp_formset.errors)
            print(mem_formset.errors)
            return self.form_invalid(form)

        doctor = form.save(commit=False)
        user = doctor.user

        user.username = form.cleaned_data["username"]
        user.email = form.cleaned_data["email"]
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.phone_number = form.cleaned_data["phone_number"]

        user.save()
        doctor.save()

          # 🔥 Save formset
        edu_formset.instance = doctor
        edu_formset.save()

        cert_formset.instance = doctor
        cert_formset.save()

        exp_formset.instance = doctor
        exp_formset.save()

        mem_formset.instance = doctor
        mem_formset.save()

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


@method_decorator(admin_required, name='dispatch')
class ListingPageCreateView(CreateView):

    model = ListingPage

    form_class = ListingPageForm

    template_name = "administrator/listing_page/form.html"

    success_url = reverse_lazy("administrator:listing-page-list")

@method_decorator(admin_required, name='dispatch')
class ListingPageListView(ListView):

    model = ListingPage

    template_name = "administrator/listing_page/list.html"

    ordering = ["slug"]


@method_decorator(admin_required, name='dispatch')
class ListingPageUpdateView(UpdateView):

    model = ListingPage

    form_class = ListingPageForm

    template_name = "administrator/listing_page/form.html"

    success_url = reverse_lazy("administrator:listing-page-list")
    
@method_decorator(admin_required, name='dispatch')
class ListingPageDeleteView(DeleteView):

    model = ListingPage

    template_name = "administrator/shared/delete.html"

    success_url = reverse_lazy("administrator:listing-page-list")


@method_decorator(admin_required, name='dispatch')
class ContentListView(ListView):

    model = Content

    template_name = "administrator/content/list.html"

    ordering = ["-published_at"]


@method_decorator(admin_required, name='dispatch')
class ContentCreateView(CreateView):

    model = Content

    form_class = ContentForm

    template_name = "administrator/content/form.html"

    success_url = reverse_lazy("administrator:content-list")

@method_decorator(admin_required, name='dispatch')
class ContentUpdateView(UpdateView):

    model = Content

    form_class = ContentForm

    template_name = "administrator/content/form.html"

    success_url = reverse_lazy("administrator:content-list")

@method_decorator(admin_required, name='dispatch')
class ContentDeleteView(DeleteView):

    model = Content

    template_name = "administrator/content/confirm_delete.html"

    success_url = reverse_lazy("administrator:content-list")


@method_decorator(admin_required, name='dispatch')
class ContentCategoryListView(ListView):

    model = ContentCategory

    template_name = "administrator/content/category_list.html"

    ordering = ["name"]


@method_decorator(admin_required, name='dispatch')
class ContentCategoryCreateView(CreateView):

    model = ContentCategory

    form_class = ContentCategoryForm

    template_name = "administrator/content/category.html"

    success_url = reverse_lazy("administrator:content-category-list")

   
@method_decorator(admin_required, name='dispatch')
class ContentCategoryUpdateView(UpdateView):

    model = ContentCategory

    form_class = ContentCategoryForm

    template_name = "administrator/content/category.html"

    success_url = reverse_lazy("administrator:content-category-list")


@method_decorator(admin_required, name='dispatch')
class ContentCategoryDeleteView(DeleteView):

    model = ContentCategory

    template_name = "administrator/content/confirm_delete.html"

    success_url = reverse_lazy("administrator:content-category-list")


@method_decorator(admin_required, name='dispatch')
class TagListView(ListView):

    model = Tag

    template_name = "administrator/content/tag_list.html"

    ordering = ["name"]

@method_decorator(admin_required, name='dispatch')
class TagCreateView(CreateView):

    model = Tag

    fields="__all__"

    template_name = "administrator/content/tag.html"

    success_url = reverse_lazy("administrator:tag-list")


@method_decorator(admin_required, name='dispatch')
class TagUpdateView(UpdateView):

    model = Tag

    fields="__all__"

    template_name = "administrator/content/tag.html"

    success_url = reverse_lazy("administrator:tag-list")

@method_decorator(admin_required, name='dispatch')
class TagDeleteView(DeleteView):

    model = Tag

    template_name = "administrator/content/confirm_delete.html"

    success_url = reverse_lazy("administrator:tag-list")


@method_decorator(admin_required, name='dispatch')
class TestimonialCreateView(CreateView):

    model = Testimonial
    form_class = TestimonialForm
    template_name = "administrator/general_sections/testimonial_manage.html"
    success_url = reverse_lazy("administrator:testimonial-list")

    def form_valid(self, form):
        messages.success(self.request, "Testimonial created successfully")
        return super().form_valid(form)
    

@method_decorator(admin_required, name='dispatch')
class TestimonialListView(ListView):
    model = Testimonial
    template_name = "administrator/general_sections/testimonial_list.html"
   

@method_decorator(admin_required, name='dispatch')
class TestimonialUpdateView(UpdateView):

    model = Testimonial
    form_class = TestimonialForm
    template_name = "administrator/general_sections/testimonial_manage.html"
    success_url = reverse_lazy("administrator:testimonial-list")

    def form_valid(self, form):
        messages.success(self.request, "Testimonial updated successfully")
        return super().form_valid(form)
    

class TestimonialDeleteView(DeleteView):
    model = Testimonial
    success_url = reverse_lazy("administrator:testimonial-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Testimonial deleted successfully")
        return super().delete(request, *args, **kwargs)



@method_decorator(admin_required, name='dispatch')
class TeamListView(ListView):
    model = TeamMember
    template_name = "administrator/general_sections/team_list.html"
  

@method_decorator(admin_required, name='dispatch')
class TeamCreateView(CreateView):

    model = TeamMember
    form_class = TeamMemberForm
    template_name = "administrator/general_sections/team_manage.html"
    success_url = reverse_lazy("administrator:team-list")

    def form_valid(self, form):
        messages.success(self.request, "Team member created successfully")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class TeamUpdateView(UpdateView):

    model = TeamMember
    form_class = TeamMemberForm
    template_name = "administrator/general_sections/team_manage.html"
    success_url = reverse_lazy("administrator:team-list")

    def form_valid(self, form):
        messages.success(self.request, "Team member updated successfully")
        return super().form_valid(form)


@method_decorator(admin_required, name='dispatch')
class TeamDeleteView(DeleteView):
    model = TeamMember
    success_url = reverse_lazy("administrator:team-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Team member deleted successfully")
        return super().delete(request, *args, **kwargs)
    


def contact_manage(request):

    contact = ContactPage.objects.first()

    if request.method == "POST":
        form = ContactPageForm(
            request.POST,
            request.FILES,
            instance=contact
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Contact details updated successfully")
            return redirect("administrator:contact-manage")

    else:
        form = ContactPageForm(instance=contact)

    return render(
        request,
        "administrator/pages/contact.html",
        {
            "form": form,
            "contact": contact
        }
    )


class ContactSubmissionListView(ListView):
    model = ContactSubmission
    template_name = "administrator/contact/submissions.html"
    context_object_name = "submissions"
    ordering = ["-created_at"]

def mark_submission_read(request, pk):

    submission = get_object_or_404(ContactSubmission, pk=pk)
    submission.is_read = True
    submission.save()

    return redirect("administrator:contact-submissions")

class ContactSubmissionDeleteView(DeleteView):
    model = ContactSubmission
    success_url = reverse_lazy("administrator:contact-submissions")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Message deleted successfully")
        return super().delete(request, *args, **kwargs)



@method_decorator(admin_required, name='dispatch')
class PackageCreateView(CreateView):

    model = Packages
    form_class = PackageCategoryForm
    template_name = "administrator/packages/form.html"
    success_url = reverse_lazy("administrator:package-list")

    # ✅ CONTEXT
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['feature_formset'] = PackageFeatureFormSet(self.request.POST)
        else:
            context['feature_formset'] = PackageFeatureFormSet()

        return context

    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()
        feature_formset = context['feature_formset']

        if not feature_formset.is_valid():
            print("Feature Errors ❌", feature_formset.errors)
            return self.form_invalid(form)

        package = form.save()

        feature_formset.instance = package
        feature_formset.save()

        messages.success(self.request, "Package  created successfully")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class PackageUpdateView(UpdateView):

    model = Packages
    form_class = PackageCategoryForm
    template_name = "administrator/packages/form.html"
    success_url = reverse_lazy("administrator:package-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['feature_formset'] = PackageFeatureFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['feature_formset'] = PackageFeatureFormSet(
                instance=self.object
            )

        return context

    @transaction.atomic
    def form_valid(self, form):

        context = self.get_context_data()
        feature_formset = context['feature_formset']

        if not feature_formset.is_valid():
            print("Feature Errors ❌", feature_formset.errors)
            return self.form_invalid(form)

        package = form.save()

        feature_formset.instance = package
        feature_formset.save()

        messages.success(self.request, "Package updated successfully")
        return super().form_valid(form)

class PackageListView(ListView):
    model = Packages
    template_name = "administrator/packages/list.html"
    context_object_name = "packages"

class PackageDeleteView(DeleteView):
    model = Packages
    template_name = "administrator/packages/confirm_delete.html"
    success_url = reverse_lazy("administrator:package-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "package deleted successfully")
        return super().delete(request, *args, **kwargs)



@method_decorator(admin_required, name='dispatch')
class InsuranceCreateView(CreateView):

    model = Insurance
    form_class = InsuranceForm
    template_name = "administrator/insurance/manage.html"
    success_url = reverse_lazy("administrator:insurance-list")

    def form_valid(self, form):
        messages.success(self.request, "Insurance created successfully")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class InsuranceUpdateView(UpdateView):

    model = Insurance
    form_class = InsuranceForm
    template_name = "administrator/insurance/manage.html"
    success_url = reverse_lazy("administrator:insurance-list")

    def form_valid(self, form):
        messages.success(self.request, "Insurance updated successfully")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class InsuranceListView(ListView):
    model = Insurance
    template_name = "administrator/insurance/list.html"
    context_object_name = "insurances"


@method_decorator(admin_required, name='dispatch')
class InsuranceDeleteView(DeleteView):
    model = Insurance
    success_url = reverse_lazy("administrator:insurance-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Insurance deleted successfully")
        return super().delete(request, *args, **kwargs)

@method_decorator(admin_required, name='dispatch')
class LegalPageCreateView(CreateView):
    model = LegalPage
    form_class = LegalPageForm
    template_name = "administrator/legal/manage.html"
    success_url = reverse_lazy("administrator:legal-list")

    def form_valid(self, form):
        messages.success(self.request, "Legal page created successfully")
        return super().form_valid(form)



@method_decorator(admin_required, name='dispatch')
class LegalPageUpdateView(UpdateView):
    model = LegalPage
    form_class = LegalPageForm
    template_name = "administrator/legal/manage.html"
    success_url = reverse_lazy("administrator:legal-list")

    def form_valid(self, form):
        messages.success(self.request, "Legal page updated successfully")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class LegalPageDeleteView(DeleteView):
    model = LegalPage
    success_url = reverse_lazy("administrator:legal-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Legal page deleted successfully")
        return super().delete(request, *args, **kwargs)

@method_decorator(admin_required, name='dispatch')   
class LegalPageListView(ListView):
    model = LegalPage
    template_name = "administrator/legal/list.html"
    context_object_name = "pages"


def global_settings_manage(request):

    settings = GlobalSettings.objects.first()   # ✅ get existing

    if request.method == "POST":

        form = GlobalSettingsForm(
            request.POST,
            request.FILES,
            instance=settings   # ✅ important
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Settings saved successfully")
            return redirect("administrator:global-settings")

        else:
            print("ERROR ❌", form.errors)

    else:
        form = GlobalSettingsForm(instance=settings)

    return render(
        request,
        "administrator/general_settings/manage.html",
        {
            "form": form,
            "settings": settings
        }
    )


class SocialLinkListView(ListView):
    model = SocialLink
    template_name = "administrator/social/list.html"
    context_object_name = "socials"


class SocialLinkCreateView(CreateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "administrator/social/manage.html"
    success_url = reverse_lazy("administrator:social-list")

    def form_valid(self, form):
        messages.success(self.request, "Social link created successfully")
        return super().form_valid(form)
    
class SocialLinkUpdateView(UpdateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "administrator/social/manage.html"
    success_url = reverse_lazy("administrator:social-list")

    def form_valid(self, form):
        messages.success(self.request, "Social link updated successfully")
        return super().form_valid(form)
    
class SocialLinkDeleteView(DeleteView):
    model = SocialLink
    success_url = reverse_lazy("administrator:social-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Social link deleted successfully")
        return super().delete(request, *args, **kwargs)


# -----------------------
# LIST VIEW
# -----------------------
class MenuGroupListView(ListView):
    model = MenuGroup
    template_name = "administrator/menu/list.html"
    context_object_name = "menus"


# -----------------------
# CREATE VIEW
# -----------------------
class MenuGroupCreateView(CreateView):
    model = MenuGroup
    form_class = MenuGroupForm
    template_name = "administrator/menu/manage.html"
    success_url = reverse_lazy("administrator:menu-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = MenuItemFormSet(self.request.POST)
        else:
            context['formset'] = MenuItemFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()

            formset.instance = self.object
            formset.save()

            return redirect(self.success_url)

        return self.form_invalid(form)


# -----------------------
# UPDATE VIEW
# -----------------------
class MenuGroupUpdateView(UpdateView):
    model = MenuGroup
    form_class = MenuGroupForm
    template_name = "administrator/menu/manage.html"
    success_url = reverse_lazy("administrator:menu-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = MenuItemFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['formset'] = MenuItemFormSet(instance=self.object)

        # 🔥 Fix Parent Dropdown (VERY IMPORTANT)
        for form in context['formset']:
            form.fields['parent'].queryset = MenuItem.objects.filter(
                menu=self.object
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()

            formset.instance = self.object
            formset.save()

            return redirect(self.success_url)

        return self.form_invalid(form)


# -----------------------
# DELETE VIEW
# -----------------------
class MenuGroupDeleteView(DeleteView):
    model = MenuGroup
    template_name = "administrator/menu/manage.html"
    success_url = reverse_lazy("administrator:menu-list")



def homepage_manage(request):

    # ✅ Get existing homepage or create new
    instance = HomePage.objects.first()

    if request.method == "POST":

        form = HomePageForm(request.POST, request.FILES, instance=instance)

        banner_formset = HomeBannerFormSet(
            
            request.POST or None,
            request.FILES or None,
            instance=instance,
            prefix='banners'
        )

        feature_formset = HomeFeatureFormSet(
            request.POST,
            request.FILES,
            instance=instance,
            prefix='features'
        )

        why_formset = WhyChooseFormSet(
            request.POST,
            request.FILES,
            instance=instance,
            prefix='whychoose'
        )

        homefaq_formset = HomeFAQFormSet(
              request.POST or None,
              instance=instance,
               prefix='faqs'
             )
        
        highlight_formset = HighlightFormSet(
                request.POST or None,
                request.FILES or None,
                instance=instance,
                prefix='highlights'
             )

        if (
            form.is_valid() and
            banner_formset.is_valid() and
            feature_formset.is_valid() and
            why_formset.is_valid()  and
            homefaq_formset.is_valid() and
            highlight_formset.is_valid()
           
        ):
            homepage = form.save()

            banner_formset.instance = homepage
            banner_formset.save()

            feature_formset.instance = homepage
            feature_formset.save()

            why_formset.instance = homepage
            why_formset.save()

            homefaq_formset.instance = homepage
            homefaq_formset.save()

            highlight_formset.instance = homepage
            highlight_formset.save()

            return redirect(reverse_lazy("administrator:homepage-manage"))
        else:

            print("FORM ERRORS:", form.errors)
            print("BANNER ERRORS:", banner_formset.errors)
            print("FEATURE ERRORS:", feature_formset.errors)
            print("WHY ERRORS:", why_formset.errors)
            print("FAQ ERRORS:", homefaq_formset.errors)
            print("highlight ERRORS:", highlight_formset.errors)
    else:
        form = HomePageForm(instance=instance)
        banner_formset = HomeBannerFormSet(
            instance=instance,
            prefix='banners'
        )

        feature_formset = HomeFeatureFormSet(
            instance=instance,
            prefix='features'
        )

        why_formset = WhyChooseFormSet(
            instance=instance,
            prefix='whychoose'
        )

        homefaq_formset =HomeFAQFormSet(
            instance=instance,
            prefix='faqs'
        )

        highlight_formset=HighlightFormSet(
             instance=instance,
             prefix='highlights'
        )
        
      
    context = {
        'form': form,
        'banner_formset': banner_formset,
        'feature_formset': feature_formset,
        'why_formset': why_formset,
        'faq_formset': homefaq_formset,
        'highlight_formset': highlight_formset,
  
      
    }

    return render(request, "administrator/pages/home.html", context)




class DoctorScheduleCreateView(CreateView):

    model = DoctorSchedule
    form_class = DoctorScheduleForm
    template_name = "administrator/schedule/form.html"
    success_url = reverse_lazy("administrator:schedule-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["formset"] = DoctorScheduleTimeFormSet(self.request.POST)
        else:
            context["formset"] = DoctorScheduleTimeFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():

            self.object = form.save()

            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)



def load_doctors_by_specialization(request):

    spec_id = request.GET.get("specialization")

    doctors = Doctor.objects.filter(
        specialization_id=spec_id
    ).select_related("user")

    data = [
        {
            "id": d.id,
            "name": f"{d.user.first_name} ({d.specialization.name})"
        }
        for d in doctors
    ]

    return JsonResponse(data, safe=False)


class DoctorScheduleListView(ListView):

    model = DoctorSchedule
    template_name = "administrator/schedule/list.html"
    context_object_name = "schedules"



class DoctorScheduleUpdateView(UpdateView):

    model = DoctorSchedule
    form_class = DoctorScheduleForm
    template_name = "administrator/schedule/form.html"

    def get_success_url(self):
        return reverse_lazy("administrator:schedule_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["formset"] = DoctorScheduleTimeFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context["formset"] = DoctorScheduleTimeFormSet(
                instance=self.object
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():

            self.object = form.save()

            formset.instance = self.object
            formset.save()

            return redirect("administrator:schedule_list")

        return self.form_invalid(form)


class DoctorScheduleDeleteView(DeleteView):

    model = DoctorSchedule
    template_name = "administrator/schedule/confirm_delete.html"
    success_url = reverse_lazy("administrator:schedule_list")




class DoctorLeaveCreateView(CreateView):

    model = DoctorLeave
    form_class = DoctorLeaveForm
    template_name = "administrator/leave/form.html"
    success_url = reverse_lazy("administrator:leave_create")

class DoctorLeaveListView(ListView):

    model = DoctorLeave
    template_name = "administrator/leave/list.html"
    context_object_name = "leaves"

    def get_queryset(self):
        return DoctorLeave.objects.select_related("doctor").order_by("-date")


class DoctorLeaveUpdateView(UpdateView):

    model = DoctorLeave
    form_class = DoctorLeaveForm
    template_name = "administrator/leave/form.html"

    def get_success_url(self):
        return reverse_lazy("administrator:leave_list")
    

class DoctorLeaveDeleteView(DeleteView):

    model = DoctorLeave
    template_name = "administrator/leave/confirm_delete.html"
    success_url = reverse_lazy("administrator:leave_list")




def booking_list(request):

    today = date.today()

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    # 🔥 BASE QUERY
    bookings = Appointment.objects.all().select_related("doctor")

    # ✅ IF NO FILTER → SHOW TODAY ONLY
    if not from_date and not to_date:
        bookings = bookings.filter(date=today)

    else:
        if from_date:
            bookings = bookings.filter(date__gte=from_date)

        if to_date:
            bookings = bookings.filter(date__lte=to_date)

    context = {
        "bookings": bookings.order_by("-date", "-time"),
        "today": today,
        "from_date": from_date,
        "to_date": to_date,
    }


    return render(request, "administrator/booking/list.html", context)



def update_booking_status(request, pk):

    if request.method == "POST":

        booking = Appointment.objects.get(id=pk)
        new_status = request.POST.get("status")

        booking.status = new_status
        booking.save()

    return redirect("administrator:booking_list")


# def update_booking_status(request, pk):

#     if request.method == "POST":

#         booking = Appointment.objects.get(id=pk)
#         new_status = request.POST.get("status")

#         # 🔥 avoid duplicate send
#         if booking.status != new_status:

#             booking.status = new_status
#             booking.save()

#             # ================= 🔥 SEND WHATSAPP TO PATIENT =================
#             phone = booking.phone

#             if phone:

#                 # ✅ ensure country code
#                 # if not phone.startswith("+"):
#                 #     phone = "+91" + phone

#                 # 🔥 MESSAGE BASED ON STATUS
#                 if new_status == "approved":

#                     message = (
#                         "Your Appointment is Confirmed\n\n"
#                         f"Doctor: {booking.doctor}\n"
#                         f"Date: {booking.date}\n"
#                         f"Time: {booking.time.strftime('%I:%M %p')}"
#                     )

#                 elif new_status == "cancelled":

#                     message = (
#                         "Your Appointment has been Cancelled\n\n"
#                         f"Doctor: {booking.doctor}\n"
#                         f"Date: {booking.date}\n"
#                         f"Time: {booking.time.strftime('%I:%M %p')}"
#                     )

#                 else:
#                     message = None

#                 # 🔥 SEND MESSAGE
#                 if message:
#                     try:
#                         send_whatsapp_message(message, phone)
#                     except Exception as e:
#                         print("WhatsApp Error:", e)

#             # ===============================================================

#     return redirect("administrator:booking_list")


def delete_booking(request, pk):

    booking = Appointment.objects.get(id=pk)
    booking.delete()

    return redirect("administrator:booking_list")

class GalleryListView(ListView):
    model = Gallery
    template_name = "administrator/gallery/list.html"
    context_object_name = "galleries"

class GalleryCreateView(CreateView):
    model = Gallery
    form_class = GalleryForm
    template_name = "administrator/gallery/form.html"
    success_url = reverse_lazy("administrator:gallery_list")

    def form_valid(self, form):
        self.object = form.save()

        files = self.request.FILES.getlist('images')

        for f in files:
            GalleryImage.objects.create(
                gallery=self.object,
                image=f
            )

        return redirect(self.success_url)


class GalleryUpdateView(UpdateView):
    model = Gallery
    form_class = GalleryForm
    template_name = "administrator/gallery/form.html"
    success_url = reverse_lazy("administrator:gallery_list")

    def form_valid(self, form):
        self.object = form.save()

        files = self.request.FILES.getlist('images')

        for f in files:
            GalleryImage.objects.create(
                gallery=self.object,
                image=f
            )

        return redirect(self.success_url)

class GalleryDeleteView(DeleteView):
    model = Gallery
    template_name = "administrator/gallery/confirm_delete.html"
    success_url = reverse_lazy("administrator:gallery_list")



def gallery_image_delete(request, pk):

    image = get_object_or_404(GalleryImage, pk=pk)
    gallery_id = image.gallery.id

    image.delete()

    return redirect('administrator:gallery_edit', pk=gallery_id)