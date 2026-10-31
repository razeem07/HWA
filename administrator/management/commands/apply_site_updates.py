"""
Applies the Elister Med website update requirements (contact details,
Pathology department, insurance, social links, doctors, blog authors,
removal of "Emergency 24/7" wording) to the database.

Safe to run more than once. Run with --dry-run to preview.

    python manage.py apply_site_updates --dry-run
    python manage.py apply_site_updates
"""
import re
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from administrator.models import (
    AboutPage, ContactPage, Content, Doctor, DoctorExpertise, GlobalSettings, HighlightItem, HomeFeature,
    HomeFAQ, HomePage, Insurance, LegalPage, ListingPage, MenuItem, Service, ServiceFAQ, SocialLink,
    Specialization, SpecializationFAQ, WhyChooseItem,
)


ADDRESS = "Al Noor Building - Al Qusais Industrial Area 3 - Al Qusais - Dubai"
EMAIL = "info@elistermed.ae"
MOBILE = "+971 54 232 0542"
LANDLINE = "+971 4 283 8398"
WHATSAPP = "971542320542"
MAP_EMBED = (
    '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4316.456279285522!2d55.393329575384904'
    '!3d25.296692977647073!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5f5d4c41cae76f%3A0x2872f85ef9de0487'
    '!2sElister%20Med%20Dubai!5e1!3m2!1sen!2sin!4v1793451525184!5m2!1sen!2sin" width="600" height="450" '
    'style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>'
)

PATHOLOGY = {
    "name": "Pathology",
    "slug": "pathology",
    "short_description": "Accurate laboratory testing and clinical pathology services to support timely diagnosis and effective treatment.",
    "hero_title": "Accurate Diagnostics for Better Healthcare Decisions",
    "hero_description": "Reliable laboratory testing and clinical pathology services, all under one roof.",
    "main_title": "Reliable, Accurate & Patient-Focused Diagnostics",
    "main_description": (
        "<p>Accurate diagnosis is the foundation of effective treatment. Laboratory "
        "results guide your doctor&rsquo;s decisions at every stage of care, from early "
        "screening to monitoring ongoing conditions.</p>\r\n\r\n"
        "<p>At Elister Med, our Pathology department provides reliable laboratory testing "
        "on site, so samples can be collected and processed without visiting another facility.</p>"
    ),
    "secondary_title": "Diagnostics You Can Rely On",
    "long_description_primary": (
        "<p>Our Pathology department supports every department at Elister Med with routine "
        "and specialised laboratory investigations, including blood tests, health screening "
        "panels and tests that help detect and monitor chronic conditions.</p>\r\n\r\n"
        "<p>Having the laboratory on site means faster results, fewer visits and better "
        "coordination between your doctor and the lab.</p>"
    ),
    "long_description_secondary": (
        "<p>We follow standard laboratory procedures and quality checks to ensure every result "
        "is accurate and dependable, supporting both patients and doctors in making informed "
        "healthcare decisions.</p>"
    ),
    "meta_title": "Pathology & Laboratory Services in Al Qusais, Dubai | Elister Med",
    "meta_description": "Accurate laboratory testing and clinical pathology services at Elister Med, Al Qusais, Dubai.",
}

LABORATORY_SERVICE = {
    "short_description": "Reliable laboratory testing and diagnostics, all under one roof.",
    "hero_description": "Reliable laboratory testing and diagnostics, all under one roof.",
    "main_description": PATHOLOGY["main_description"],
    "long_description_primary": PATHOLOGY["long_description_primary"],
    "long_description_secondary": PATHOLOGY["long_description_secondary"],
}

PATHOLOGY_FAQ = (
    "What does the Pathology department do?",
    "Our Pathology department carries out laboratory tests on samples such as blood and "
    "urine to help doctors diagnose, monitor and treat medical conditions.",
)

# Elister Group (parent company) and the Elister Privilege Card (product) are
# separate names and are intentionally not changed.
BRAND_FIELDS = [
    (ListingPage, "banner_title"),
    (AboutPage, "chairman_description"),
    (LegalPage, "content"),
    (HomePage, "why_choose_subtitle"),
    (HomePage, "highlights_subtitle"),
    (HomePage, "highlights_description"),
]

BRAND_FIXES = [
    (r"Eleister Med hospital", "Elister Med"),
    (r"Eleister", "Elister"),
    (r"Elister (?:Hospital|Healthcare)", "Elister Med"),
    (r"Elistermed Polyclinic(?: \( \))?", "Elister Med"),
    (r"\bElistermed\b", "Elister Med"),
    (r"Why Choose Elister(?! Med)", "Why Choose Elister Med"),
    (r"\bElister's", "Elister Med's"),
]

NEW_INSURANCES = ["SAICO", "INAYA", "NGI"]

NEW_SOCIAL_LINKS = [
    ("facebook", "https://www.facebook.com/profile.php?id=61574008442998", "fa-brands fa-facebook-f", 0, True),
    ("instagram", "https://www.instagram.com/elistermeddubai", "fa-brands fa-instagram", 1, True),
    ("linkedin", "https://www.linkedin.com/company/elistermed/", "fa-brands fa-linkedin-in", 2, True),
    # Placeholder until the clinic supplies the official account; stays
    # inactive (hidden) until updated in the admin.
    ("tiktok", "https://www.tiktok.com/", "fa-brands fa-tiktok", 3, False),
]

DOCTOR_IMAGES = Path(__file__).resolve().parents[1] / "doctor_images"
DOCTOR_HERO_BANNER = "uploads/doctors/banner_inner_cardio.jpg"

NEW_DOCTORS = [
    {"username": "saheeda.nezrin", "first_name": "Saheeda", "last_name": "Nezrin",
     "slug": "dr-saheeda-nezrin", "image": "saheeda-nezrin.jpg"},
    {"username": "ranjana", "first_name": "Ranjana", "last_name": "",
     "slug": "dr-ranjana", "image": "ranjana.jpg"},
    {"username": "asmina", "first_name": "Asmina", "last_name": "",
     "slug": "dr-asmina", "image": "asmina.jpg"},
    {"username": "bincy", "first_name": "Bincy", "last_name": "",
     "slug": "dr-bincy", "image": "bincy.jpg"},
]

# General profile text only: experience, qualifications and statistics are left
# empty until the clinic confirms them, and the pages hide empty items.
GP_EXPERTISE = [
    "General medical consultations",
    "Preventive health checks",
    "Acute illness care",
    "Long-term condition follow-up",
    "Health and lifestyle advice",
]


def gp_profile(name):
    return {
        "designation": "General Practitioner",
        "specialized_in": "General Medicine",
        "languages": "English",
        "hero_title": "General Practitioner at Elister Med",
        "hero_description": f"{name} provides general medical care for individuals and families at Elister Med, Dubai.",
        "short_bio": (
            f"{name} is a General Practitioner at Elister Med, providing consultations, "
            "preventive care and follow-up for patients and families."
        ),
        "full_bio": (
            f"<p>{name} is a General Practitioner at Elister Med in Al Qusais, Dubai, offering "
            "consultations for common health concerns, preventive check-ups and ongoing care.</p>"
            "<p>As a first point of contact, a General Practitioner assesses symptoms, arranges "
            "investigations where needed and refers patients to the right specialist, working "
            "closely with the other departments at Elister Med.</p>"
        ),
        "meta_title": f"{name} - General Practitioner in Al Qusais, Dubai | Elister Med",
        "meta_description": f"Book a consultation with {name}, General Practitioner at Elister Med, Al Qusais, Dubai.",
        "profile_image_alt": f"{name}, General Practitioner at Elister Med",
        "doctor_hero_banner": DOCTOR_HERO_BANNER,
        "is_active": True,
    }


class Command(BaseCommand):
    help = "Apply the Elister Med website update requirements to the database."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show changes without saving them.")

    def log(self, msg):
        self.stdout.write(f"  - {msg}")

    def set_fields(self, obj, label, **values):
        changed = {k: v for k, v in values.items() if getattr(obj, k) != v}
        if changed:
            for k, v in changed.items():
                setattr(obj, k, v)
            obj.save()
            self.log(f"{label}: updated {', '.join(changed)}")

    def handle(self, *args, dry_run=False, **options):
        self.dry_run = dry_run
        with transaction.atomic():
            self.contact_details()
            self.brand_name()
            pathology = self.pathology()
            self.emergency_wording()
            self.insurances()
            self.social_links()
            self.doctors(pathology)
            self.blog_authors()
            self.security_and_cleanup()

            if dry_run:
                transaction.set_rollback(True)
                self.stdout.write(self.style.WARNING("Dry run: no changes saved."))
            else:
                self.stdout.write(self.style.SUCCESS("Site updates applied."))

    # 1 & 8. Contact details
    def contact_details(self):
        self.stdout.write("Contact details")
        gs = GlobalSettings.objects.first()
        if gs:
            self.set_fields(
                gs, "Global settings",
                address=ADDRESS, email_primary=EMAIL,
                phone_primary=MOBILE, phone_secondary=LANDLINE,
                whatsapp_number=WHATSAPP,
            )
        cp = ContactPage.objects.first()
        if cp:
            self.set_fields(
                cp, "Contact page",
                address=f"<p>{ADDRESS}</p>", email_primary=EMAIL,
                phone_primary=MOBILE, phone_secondary=LANDLINE,
                whatsapp_number=f"+{WHATSAPP}", emergency_info="",
                map_embed=MAP_EMBED,
            )

    # Use "Elister Med" as the clinic name everywhere
    def brand_name(self):
        self.stdout.write("Brand name")
        for model, field in BRAND_FIELDS:
            for obj in model.objects.all():
                value = getattr(obj, field) or ""
                fixed = value
                for pattern, replacement in BRAND_FIXES:
                    fixed = re.sub(pattern, replacement, fixed)
                self.set_fields(obj, f"{model.__name__} #{obj.pk}", **{field: fixed})

    # 2. Pathology replaces Allied Services
    def pathology(self):
        self.stdout.write("Departments")
        spec = (
            Specialization.objects.filter(slug="pathology").first()
            or Specialization.objects.filter(slug="allied-services").first()
        )
        if spec is None:
            self.log("Allied Services / Pathology department not found - skipped")
            return None

        # Saving a new slug records a redirect from /allied-services/.
        self.set_fields(spec, "Specialization", **PATHOLOGY)

        for faq in SpecializationFAQ.objects.filter(specialization=spec, question__icontains="allied"):
            self.set_fields(faq, f"Specialization FAQ #{faq.pk}", question=PATHOLOGY_FAQ[0], answer=PATHOLOGY_FAQ[1])

        lab = Service.objects.filter(slug="laboratory").first()
        if lab:
            self.set_fields(lab, "Laboratory service", **LABORATORY_SERVICE)
            for faq in ServiceFAQ.objects.filter(service=lab, question__icontains="allied"):
                self.set_fields(faq, f"Service FAQ #{faq.pk}", question=PATHOLOGY_FAQ[0], answer=PATHOLOGY_FAQ[1])

        # The pharmacy is not part of Pathology; list it under General Medicine.
        pharmacy = Service.objects.filter(slug="in-house-pharmacy", specialization=spec).first()
        general = Specialization.objects.filter(slug="general-medicine").first()
        if pharmacy and general:
            self.set_fields(pharmacy, "In-House Pharmacy service", specialization=general)

        for item in MenuItem.objects.filter(url__icontains="allied-services"):
            self.set_fields(item, f"Menu item #{item.pk}", title="Pathology", url="/specializations/pathology/")

        for item in WhyChooseItem.objects.filter(title__iexact="Allied Services"):
            self.set_fields(item, f"Home 'why choose' item #{item.pk}", title="Pathology")

        return spec

    # 1 & 8. Remove "Emergency Help 24/7" wording
    def emergency_wording(self):
        self.stdout.write("Emergency wording")
        for model, label in ((HomeFeature, "Home feature"), (HighlightItem, "Home highlight")):
            for obj in model.objects.filter(title__icontains="emergency"):
                self.log(f"{label} '{obj.title}': deleted")
                obj.delete()

        for page in ListingPage.objects.all():
            values = {}
            if re.search(r"emergency|24\s*[/*x]\s*7", page.footer_description, re.I):
                values["footer_description"] = "Schedule your appointment today and experience the difference of patient-centered care"
            if "emergency" in page.page_cta.lower() or not page.page_cta.strip():
                values["page_cta"] = "Book an appointment"
            if values:
                self.set_fields(page, f"Listing page '{page.slug}'", **values)

        for service in Service.objects.filter(slug="emergency-care-trauma", is_active=True):
            self.set_fields(service, f"Service '{service.name}'", is_active=False)

    # 3. Insurance providers
    def insurances(self):
        self.stdout.write("Insurance")
        for name in NEW_INSURANCES:
            _, created = Insurance.objects.get_or_create(
                name=name,
                defaults={"short_description": name, "long_description": name, "is_active": True},
            )
            if created:
                self.log(f"Insurance '{name}': added")

    # 4. Social media
    def social_links(self):
        self.stdout.write("Social links")
        for name, url, icon, order, active in NEW_SOCIAL_LINKS:
            link, created = SocialLink.objects.get_or_create(
                name=name,
                defaults={"url": url, "icon_class": icon, "order": order, "is_active": active},
            )
            if created:
                self.log(f"Social link '{name}': added ({'active' if active else 'inactive until the real URL is set'})")
            elif active:
                self.set_fields(link, f"Social link '{name}'", url=url, icon_class=icon, order=order, is_active=True)

    # 5. Doctors
    def doctors(self, pathology):
        self.stdout.write("Doctors")
        User = get_user_model()

        for doctor in Doctor.objects.filter(user__first_name__icontains="Surumi", is_active=True):
            self.set_fields(doctor, f"Dr. {doctor.user.get_full_name()}", is_active=False)

        # Dr. Fatma is the clinic's clinical pathologist.
        if pathology:
            for doctor in Doctor.objects.filter(slug="clinical-pathology").exclude(specialization=pathology):
                self.set_fields(doctor, f"Dr. {doctor.user.get_full_name()}", specialization=pathology)

        general = Specialization.objects.filter(slug="general-medicine").first()
        if general is None:
            self.log("General Medicine department not found - new doctors skipped")
            return

        for data in NEW_DOCTORS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={"first_name": data["first_name"], "last_name": data["last_name"],
                          "is_doctor": True, "is_patient": False},
            )
            if created:
                user.set_unusable_password()
                user.save()

            name = f"Dr. {user.get_full_name()}"
            doctor = Doctor.objects.filter(user=user).first()
            if doctor is None:
                doctor = Doctor.objects.create(
                    user=user, branch=general.branch, specialization=general,
                    slug=data["slug"], years_of_experience=0, is_active=False,
                )
                self.log(f"{name}: added")

            self.set_fields(doctor, name, specialization=general, slug=data["slug"], **gp_profile(name))

            if not doctor.profile_image and not self.dry_run:
                with open(DOCTOR_IMAGES / data["image"], "rb") as image:
                    doctor.profile_image.save(data["image"], File(image), save=True)
                self.log(f"{name}: profile image added")

            for title in GP_EXPERTISE:
                DoctorExpertise.objects.get_or_create(doctor=doctor, title=title)

    # Doctor accounts no longer use the old shared default password
    def security_and_cleanup(self):
        self.stdout.write("Security and clean-up")
        for doctor in Doctor.objects.select_related("user"):
            if doctor.user.check_password("doctor123"):
                doctor.user.set_unusable_password()
                doctor.user.save()
                self.log(f"Dr. {doctor.user.get_full_name()}: default password removed")

        placeholders = HomeFAQ.objects.filter(question__regex=r"^q[0-9]+$")
        if placeholders.exists():
            self.log(f"Home FAQ: removed {placeholders.count()} placeholder rows")
            placeholders.delete()

    # 7. Blog / article author
    def blog_authors(self):
        self.stdout.write("Blog authors")
        mili = Doctor.objects.filter(user__first_name__iexact="Mili").first()
        if mili is None:
            self.log("Dr. Mili not found - skipped")
            return
        for content in Content.objects.filter(published_by__user__first_name__icontains="Ramesh"):
            self.set_fields(content, f"{content.content_type} '{content.title[:40]}'", published_by=mili)
