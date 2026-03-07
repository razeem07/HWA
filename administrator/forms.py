from django import forms
from .models import Branch,Specialization,Doctor
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
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'main_title': forms.TextInput(attrs={'class': 'form-control'}),
            'main_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),

            'secondary_title': forms.TextInput(attrs={'class': 'form-control'}),

            

            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'og_title': forms.TextInput(attrs={'class': 'form-control'}),
            'og_description': forms.TextInput(attrs={'class': 'form-control'}),

            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'canonical_url': forms.URLInput(attrs={'class': 'form-control'}),

            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


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


# class DoctorForm(forms.ModelForm):

    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()

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