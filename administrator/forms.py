from django import forms
from django.forms import inlineformset_factory
from .models import Branch,Specialization,Doctor,ListingPage,Content,ContentCategory,AboutPage,DoctorEducation,DoctorCertification,DoctorExpertise,DoctorMembership,SpecializationService,SpecializationFAQ,TeamMember,Testimonial,ContactPage,Service,ServiceFAQ,PackageCategory,PackageCategoryFAQ,PackageProduct,PackageFeature,Insurance,LegalPage,GlobalSettings,SocialLink,MenuGroup,MenuItem,HomePage,HomeBanner,HomeFeature,WhyChooseItem,HomeFAQ,HighlightItem,DoctorSchedule,DoctorScheduleTime,DoctorLeave
from django.contrib.auth import get_user_model

User = get_user_model()



class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'description', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter branch name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Branch description',
                'rows': 4
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class ListingPageForm(forms.ModelForm):

    class Meta:
        model = ListingPage
        exclude = ["created_at"]

        widgets = {

            "slug": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "banner_title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "banner_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),

            "page_title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

             "page_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),

            
             "page_cta": forms.Textarea(
                attrs={"class": "form-control"}
            ),



            "meta_title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "meta_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),

            "canonical_url": forms.URLInput(
                attrs={"class": "form-control"}
            ),

            "og_title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "og_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = "__all__"

class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = [
            'branch',
            'name',
            'short_description',
            'icon',
            'featured_image',
            'featured_image_alt',

            'hero_title',
            'hero_description',
            'hero_banner',
            'hero_banner_alt',

            'main_title',
            'main_image',
            'main_image_alt',
            'main_description',

            'secondary_title',
            'secondary_image',
            'secondary_image_alt',

            'long_description_primary',
            'long_description_secondary',

            'meta_title',
            'primary_keywords',
            'secondary_keywords',
            'meta_description',
            'slug',
            'canonical_url',
            'og_title',
            'og_description',
            'og_image',

            'is_active',
        ]

        widgets = {
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
             'name': forms.TextInput(attrs={"class": "form-control", "required": True}),
            'featured_image_alt':forms.TextInput(attrs={'class':'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hero_banner_alt':forms.TextInput(attrs={'class':'form-control'}),

            'hero_title': forms.TextInput(attrs={"class": "form-control", "required": True}),
            'hero_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'main_title': forms.TextInput(attrs={"class": "form-control", "required": True}),
            'main_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, "required": True}),
            'main_image_alt':forms.TextInput(attrs={'class':'form-control'}),

            'secondary_title': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_image_alt':forms.TextInput(attrs={'class':'form-control'}),

            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'og_title': forms.TextInput(attrs={'class': 'form-control'}),
            'og_description': forms.TextInput(attrs={'class': 'form-control'}),

            'slug': forms.TextInput(attrs={'class': 'form-control',"required": True}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-control'}),

            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def clean(self):

        cleaned_data = super().clean()

        required_fields = [
            "name",
            "short_description",
            "featured_image",
            "hero_title",
            "hero_banner",
            "main_title",
            "main_description",
            "slug"
        ]

        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This field is required.")

        return cleaned_data

    def clean_slug(self):

       slug = self.cleaned_data.get("slug")
       if Specialization.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
        raise forms.ValidationError("Slug already exists.")
       return slug
       
ServiceFormSet = inlineformset_factory(
    Specialization,
    SpecializationService,
    fields=('title', 'description', 'icon'),
    extra=1,
    can_delete=True
)

FAQFormSet = inlineformset_factory(
    Specialization,
    SpecializationFAQ,
    fields=('question', 'answer'),
    extra=1,
    can_delete=True
)



class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = [
            'specialization',
            'name',
            'short_description',
            'icon',
            'featured_image',
            'featured_image_alt',
            'hero_title',
            'hero_description',
            'hero_banner',
            'hero_banner_alt',
            'main_title',
            'main_image',
            'main_image_alt',
            'main_description',
            'long_description_primary',
            'long_description_secondary',
            'is_active'
        ]

        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'main_title': forms.TextInput(attrs={'class': 'form-control'}),
            'main_description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'og_title': forms.TextInput(attrs={'class': 'form-control'}),
            'og_description': forms.TextInput(attrs={'class': 'form-control'}),

            'slug': forms.TextInput(attrs={'class': 'form-control',"required": True}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

ServiceFAQFormSet = inlineformset_factory(
    Service,
    ServiceFAQ,
    fields=('question', 'answer', 'is_active'),
    extra=1,
    can_delete=True
)


class DoctorForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


          # Apply bootstrap styling to all fields automatically
        for field_name, field in self.fields.items():

           if field.widget.__class__.__name__ == "CheckboxInput":
              field.widget.attrs["class"] = "form-check-input"
           else:
             field.widget.attrs["class"] = "form-control"

        # Default: no specialization
        self.fields["specialization"].queryset = Specialization.objects.none()

        # Case 1: Editing existing doctor
        if self.instance and self.instance.pk:

            self.fields["specialization"].queryset = Specialization.objects.filter(
                branch=self.instance.branch
            )

        # Case 2: POST request (user changed branch)
        if "branch" in self.data:

            try:
                branch_id = int(self.data.get("branch"))

                self.fields["specialization"].queryset = Specialization.objects.filter(
                    branch_id=branch_id
                )

            except (ValueError, TypeError):
                pass

    class Meta:
        model = Doctor
        exclude = ["user", "created_at"]

        widgets = {

            "designation": forms.TextInput(attrs={"class": "form-control"}),

            "years_of_experience": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "specialized_in": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "languages": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "procedures": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),

            "short_bio": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),

        }



EducationFormSet = inlineformset_factory(
    Doctor,                  # parent model
    DoctorEducation,         # child model
    fields=('degree','specialization_in', 'institution', 'year'),
    extra=1,                 # show 1 empty form
    can_delete=True          # allow delete
)

CertificationFormSet = inlineformset_factory(
    Doctor, DoctorCertification,
    fields=('name',),
    extra=1, can_delete=True
)

ExpertiseFormSet = inlineformset_factory(
    Doctor, DoctorExpertise,
    fields=('title',),
    extra=1, can_delete=True
)

MembershipFormSet = inlineformset_factory(
    Doctor, DoctorMembership,
    fields=('name',),
    extra=1, can_delete=True
)


class ContentForm(forms.ModelForm):

    class Meta:

        model = Content

        exclude = ["created_at", "updated_at"]

        widgets = {

            "content_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "short_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),

            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}
            ),

            "category": forms.Select(
                attrs={"class": "form-select"}
            ),

            # "tags": forms.SelectMultiple(
            #     attrs={"class": "form-select"}
            # ),

            'tags': forms.CheckboxSelectMultiple(),

            "published_by": forms.Select(
                attrs={"class": "form-select"}
            ),

            "published_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),

            "slug": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "meta_title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "meta_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),

            "canonical_url": forms.URLInput(
                attrs={"class": "form-control"}
            ),

            "og_title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "og_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class ContentCategoryForm(forms.ModelForm):
     class Meta: 
        model = ContentCategory 
        fields = ['name', 'description', 'is_active'] 
        widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Enter category name' }), 
                   'description': forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': 'description', 'rows': 4 }),
                     'is_active': forms.CheckboxInput(attrs={ 'class': 'form-check-input' }), }


class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial
        fields = ['name', 'designation', 'image', 'short_description', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TeamMemberForm(forms.ModelForm):

    class Meta:
        model = TeamMember
        fields = ['name', 'designation', 'image', 'short_description', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ContactPageForm(forms.ModelForm):

    class Meta:
        model = ContactPage
        fields = [
            'address',
            'phone_primary',
            'phone_secondary',
            'whatsapp_number',
            'email_primary',
            'email_secondary',
            'map_embed',
            'emergency_info'
        ]

        widgets = {
            'phone_primary': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_secondary': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email_primary': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_secondary': forms.EmailInput(attrs={'class': 'form-control'}),
            'map_embed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PackageCategoryForm(forms.ModelForm):

    class Meta:
        model = PackageCategory
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_description': forms.Textarea(attrs={'class': 'form-control'}),
            'main_title': forms.TextInput(attrs={'class': 'form-control'}),
            'main_description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

PackageCategoryFAQFormSet = inlineformset_factory(
    PackageCategory,
    PackageCategoryFAQ,
    fields=('question', 'answer', 'is_active'),
    extra=1,
    can_delete=True
)


class PackageProductForm(forms.ModelForm):

    class Meta:
        model = PackageProduct
        fields = '__all__'

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parameters': forms.Textarea(attrs={'class': 'form-control'}),
            'actual_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'offer_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


PackageFeatureFormSet = inlineformset_factory(
    PackageProduct,
    PackageFeature,
    fields=('feature',),
    extra=1,
    can_delete=True
)

class InsuranceForm(forms.ModelForm):

    class Meta:
        model = Insurance
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),

            "short_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "long_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),

            "featured_image_alt": forms.TextInput(attrs={
                "class": "form-control"
            }),

           
        }

class LegalPageForm(forms.ModelForm):

    class Meta:
        model = LegalPage
        fields = "__all__"

        widgets = {
            "content_type": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }

class GlobalSettingsForm(forms.ModelForm):

    class Meta:
        model = GlobalSettings
        fields = "__all__"


class SocialLinkForm(forms.ModelForm):

    class Meta:
        model = SocialLink
        fields = "__all__"


# -----------------------
# Menu Group Form
# -----------------------
class MenuGroupForm(forms.ModelForm):
    class Meta:
        model = MenuGroup
        fields = ['name', 'slug', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# -----------------------
# Menu Item Form
# -----------------------
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'parent',
            'title',
            'url',
            'icon_class',
            'order',
            'is_active'
        ]
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'icon_class': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# -----------------------
# Inline Formset
# -----------------------
MenuItemFormSet = inlineformset_factory(
    MenuGroup,
    MenuItem,
    form=MenuItemForm,
    extra=1,           # how many empty forms to show
    can_delete=True
)


# =========================
# MAIN FORM
# =========================
class HomePageForm(forms.ModelForm):

    class Meta:
        model = HomePage
        fields = "__all__"

        widgets = {
            # BASIC
            'title': forms.TextInput(attrs={'class': 'form-control'}),

            # ABOUT
            'about_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'about_title': forms.TextInput(attrs={'class': 'form-control'}),
            'about_description': forms.Textarea(attrs={'class': 'form-control'}),

            # SPECIALIZATION
            'specialization_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization_title': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization_description': forms.Textarea(attrs={'class': 'form-control'}),

            # STAFF
            'staff_title': forms.TextInput(attrs={'class': 'form-control'}),
            'staff_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'staff_description': forms.Textarea(attrs={'class': 'form-control'}),

            # WHY CHOOSE
            'why_choose_title': forms.TextInput(attrs={'class': 'form-control'}),
            'why_choose_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'why_choose_description': forms.Textarea(attrs={'class': 'form-control'}),

            # BLOG
            'blog_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'blog_title': forms.TextInput(attrs={'class': 'form-control'}),
            'blog_description': forms.Textarea(attrs={'class': 'form-control'}),

            # ARTICLE
            'article_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'article_title': forms.TextInput(attrs={'class': 'form-control'}),
            'article_description': forms.Textarea(attrs={'class': 'form-control'}),

            # FAQ
            'faq_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'faq_title': forms.TextInput(attrs={'class': 'form-control'}),
            'faq_description': forms.Textarea(attrs={'class': 'form-control'}),

            # TESTIMONIAL
            'testimonial_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'testimonial_title': forms.TextInput(attrs={'class': 'form-control'}),
            'testimonial_description': forms.Textarea(attrs={'class': 'form-control'}),

            # PARALLAX
            'parallax_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'parallax_title': forms.TextInput(attrs={'class': 'form-control'}),
            'parallax_description': forms.Textarea(attrs={'class': 'form-control'}),
            'parallax_cta': forms.TextInput(attrs={'class': 'form-control'}),
        }

class HomeBannerForm(forms.ModelForm):

    class Meta:
        model = HomeBanner
        fields = ['title', 'description', 'image', 'image_alt', 'order']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image_alt': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }



HomeBannerFormSet = inlineformset_factory(
    HomePage,
    HomeBanner,
    form=HomeBannerForm,
    extra=1,
    can_delete=True
)

class HomeFeatureForm(forms.ModelForm):

    class Meta:
        model = HomeFeature
        fields = ['title', 'image', 'order']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

HomeFeatureFormSet = inlineformset_factory(
    HomePage,
    HomeFeature,
    form=HomeFeatureForm,
    extra=1,
    can_delete=True
)


class WhyChooseItemForm(forms.ModelForm):

    class Meta:
        model = WhyChooseItem
        fields = ['image', 'title', 'description', 'order']

        widgets = {
           
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


WhyChooseFormSet = inlineformset_factory(
    HomePage,
    WhyChooseItem,
    form=WhyChooseItemForm,
    extra=1,
    can_delete=True
)



    
class HomeFAQForm(forms.ModelForm):

    class Meta:
        model = HomeFAQ
        fields = ['question', 'answer', 'order']

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    



HomeFAQFormSet = inlineformset_factory(
    HomePage,
    HomeFAQ,
    form=HomeFAQForm,
    extra=1,
    can_delete=True
)


class HighlightItemForm(forms.ModelForm):

    class Meta:
        model = HighlightItem
        fields = ['image', 'title', 'description', 'order']


HighlightFormSet = inlineformset_factory(
    HomePage,
    HighlightItem,
    form=HighlightItemForm,
    extra=1,
    can_delete=True
)

#=============Appointment System================#


class DoctorScheduleForm(forms.ModelForm):

    class Meta:
        model = DoctorSchedule
        fields = ["specialization", "doctor"]

        widgets = {
            "specialization": forms.Select(attrs={"class": "form-control"}),
            "doctor": forms.Select(attrs={"class": "form-control"}),
        }


class DoctorScheduleTimeForm(forms.ModelForm):

    class Meta:
        model = DoctorScheduleTime
        fields = ["day_of_week", "start_time", "end_time", "slot_duration", "is_active"]

        widgets = {
            "day_of_week": forms.Select(attrs={"class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "slot_duration": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class DoctorScheduleForm(forms.ModelForm):

    class Meta:
        model = DoctorSchedule
        fields = ["specialization", "doctor"]

        widgets = {
            "specialization": forms.Select(attrs={"class": "form-control"}),
            "doctor": forms.Select(attrs={"class": "form-control"}),
        }

DoctorScheduleTimeFormSet = inlineformset_factory(
    DoctorSchedule,
    DoctorScheduleTime,
    form=DoctorScheduleTimeForm,
    extra=1,
    can_delete=True
)



class DoctorLeaveForm(forms.ModelForm):

    class Meta:
        model = DoctorLeave
        fields = "__all__"

        widgets = {
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "is_full_day": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "reason": forms.TextInput(attrs={"class": "form-control"}),
        }
    
    def clean(self):
       cleaned_data = super().clean()

       is_full_day = cleaned_data.get("is_full_day")
       start = cleaned_data.get("start_time")
       end = cleaned_data.get("end_time")

       if not is_full_day:
        if not start or not end:
            raise forms.ValidationError("Start and End time required for partial leave")

        if start >= end:
            raise forms.ValidationError("End time must be greater than start time")

       return cleaned_data

