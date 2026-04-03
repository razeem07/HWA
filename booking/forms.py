from django import forms
from .models import Appointment
from administrator.models import Specialization, Doctor
from datetime import date,timedelta


SLOT_CHOICES = [
    ("10:00", "10:00 AM"),
    ("11:00", "11:00 AM"),
    ("12:00", "12:00 PM"),
    ("2:00",   "2:00 PM"),
    ("4:00",   "4:00 PM"),
]


class AppointmentForm(forms.Form):

    today = date.today()
    max_date = today + timedelta(days=7)
   # STEP 1
    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.Select(attrs={"class": "form-select mb-4","id": "id_specialization"})
    )

    # STEP 2
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.none(),  # 🔥 initially empty
        widget=forms.Select(attrs={"class": "form-select mb-4","id": "id_doctor"})
    )

    # STEP 3
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control mb-4",
              "id": "id_date",
              "min": date.today().isoformat(),
              "max":max_date.isoformat()
        })
    )

    time = forms.ChoiceField(
       choices=[],   # 🔥 IMPORTANT (empty initially)
       widget=forms.Select(attrs={
        "class": "form-select mb-4",
        "id": "id_time"
       })
    )

    # STEP 4 (USER DETAILS)
    first_name = forms.CharField(widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name"
        })
    )
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))

    # 🔥 DYNAMIC DOCTOR LOADING (WITHOUT AJAX)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "specialization" in self.data:
            try:
                spec_id = int(self.data.get("specialization"))
                self.fields["doctor"].queryset = Doctor.objects.filter(
                    specialization_id=spec_id
                )
            except:
                pass

    def clean_date(self):
      selected_date = self.cleaned_data.get("date")

      today = date.today()
      max_date = today + timedelta(days=7)

      if selected_date < today:
        raise forms.ValidationError("Past date not allowed")

      if selected_date > max_date:
        raise forms.ValidationError("Booking allowed only within 7 days")

      return selected_date

