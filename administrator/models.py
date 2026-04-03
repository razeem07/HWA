from django.db import models
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.utils.text import slugify


# Create your models here.

class SEOModel(models.Model):

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True)
    primary_keywords = models.CharField(max_length=255, blank=True)
    secondary_keywords = models.CharField(max_length=255, blank=True)

    # Slug
    slug = models.SlugField(unique=True)

    # Open Graph
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="seo/og/", blank=True, null=True)

    class Meta:
        abstract = True
    
    def generate_slug(self):
        """
        Override this method in child models
        """
        return self.slug

    def generate_slug(self):
        """
        Override this method in child models
        """
        return self.slug

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.generate_slug())

        if self.pk:
            old = self.__class__.objects.get(pk=self.pk)

            if old.slug != self.slug:
                Redirect.objects.create(
                    model_name=self.__class__.__name__.lower(),
                    old_slug=old.slug,
                    new_slug=self.slug
                )

        super().save(*args, **kwargs)


class ListingPage(SEOModel):

    banner_title = models.CharField(max_length=255)

    banner_description = models.TextField(blank=True)

    banner_image = models.ImageField(
     
        upload_to='uploads/listing_banner/', blank=True, null=True
    )

    footer_title = models.CharField(max_length=255)

    footer_description = models.TextField(blank=True)

    page_title = models.CharField(max_length=255)

    page_description = models.TextField(blank=True)

    page_cta = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

class Redirect(models.Model):

    model_name = models.CharField(max_length=50, blank=True)

    old_slug = models.SlugField()
    new_slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.old_slug} → {self.new_slug}"


class AboutPage(SEOModel):


    title = models.CharField(max_length=200)

    # 🔹 Images
    image_one = models.ImageField(
        upload_to='uploads/about/',
        blank=True,
        null=True
    )

    image_two = models.ImageField(
        upload_to='uploads/about/',
        blank=True,
        null=True
    )

    # 🔹 Content Sections
    section_one = RichTextUploadingField(blank=True, null=True)
    section_two = RichTextUploadingField(blank=True, null=True)
    section_three = RichTextUploadingField(blank=True, null=True)
    section_four = RichTextUploadingField(blank=True, null=True)

    # 🔹 Meta
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Branch(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Specialization(SEOModel):

    # -------------------------
    # RELATIONSHIP
    # -------------------------
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='specializations'
    )

    # -------------------------
    # BASIC INFO
    # -------------------------
    name = models.CharField(max_length=200)
    short_description = models.TextField(blank=True)

    icon = models.ImageField(upload_to='uploads/specializations/', blank=True, null=True)
    featured_image = models.ImageField(upload_to='uploads/specializations/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # HERO SECTION
    # -------------------------
    hero_title = models.CharField(max_length=255, blank=True)
    hero_description = models.TextField(blank=True)
    hero_banner = models.ImageField(upload_to='uploads/specializations/', blank=True, null=True)
    hero_banner_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # MAIN CONTENT
    # -------------------------
    main_title = models.CharField(max_length=255, blank=True)
    main_image = models.ImageField(upload_to='uploads/specializations/', blank=True, null=True)
    main_image_alt = models.CharField(max_length=255, blank=True)
    main_description = RichTextUploadingField(blank=True)

    secondary_title = models.CharField(max_length=255, blank=True)
    secondary_image = models.ImageField(upload_to='uploads/specializations/', blank=True, null=True)
    secondary_image_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # LONG CONTENT (RICH TEXT)
    # -------------------------
    long_description_primary = RichTextUploadingField(blank=True)
    long_description_secondary = RichTextUploadingField(blank=True)


    # -------------------------
    # STATUS & CONTROL
    # -------------------------
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_slug(self):
        return self.name
  

    # -------------------------
    # META
    # -------------------------
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"

    def __str__(self):
        return self.name


class SpecializationService(models.Model):

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name="services"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    icon = models.ImageField(
        upload_to="uploads/specializations/services/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
    

class SpecializationFAQ(models.Model):

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name="faqs"
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    


class Service(SEOModel):

    # -------------------------
    # RELATIONSHIP
    # -------------------------
    specialization = models.ForeignKey(
        "Specialization",
        on_delete=models.CASCADE,
        related_name="featured_services"
    )

    # -------------------------
    # BASIC INFO
    # -------------------------
    name = models.CharField(max_length=200)

    short_description = models.TextField(blank=True)

    icon = models.ImageField(
        upload_to='uploads/services/',
        blank=True,
        null=True
    )

    featured_image = models.ImageField(
        upload_to='uploads/services/',
        blank=True,
        null=True
    )

    featured_image_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # HERO SECTION
    # -------------------------
    hero_title = models.CharField(max_length=255, blank=True)

    hero_description = models.TextField(blank=True)

    hero_banner = models.ImageField(
        upload_to='uploads/services/',
        blank=True,
        null=True
    )

    hero_banner_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # MAIN CONTENT
    # -------------------------
    main_title = models.CharField(max_length=255, blank=True)

    main_image = models.ImageField(
        upload_to='uploads/services/',
        blank=True,
        null=True
    )

    main_image_alt = models.CharField(max_length=255, blank=True)

    main_description = RichTextUploadingField(blank=True)

    # -------------------------
    # LONG CONTENT
    # -------------------------
    long_description_primary = RichTextUploadingField(blank=True)
    long_description_secondary = RichTextUploadingField(blank=True)


    # -------------------------
    # STATUS
    # -------------------------
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # SLUG
    # -------------------------
    def generate_slug(self):
        return self.name

    # -------------------------
    # META
    # -------------------------
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name


class ServiceFAQ(models.Model):

    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="faqs"
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class Doctor(SEOModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name="doctors"
    )

    hero_title=models.CharField(max_length=255, blank=True)
    hero_description=models.TextField(max_length=255, blank=True)
    doctor_hero_banner = models.ImageField(upload_to='uploads/doctors/', blank=True, null=True)
    doctor_hero_banner_alt = models.CharField(max_length=255, blank=True)


    designation = models.CharField(
        max_length=200,
        blank=True
    )

    years_of_experience = models.PositiveIntegerField(
        help_text="Years of experience"
    )

    profile_image = models.ImageField(
        upload_to="uploads/doctors/profile/",
        blank=True,
        null=True
    )

    profile_image_alt = models.CharField(max_length=255, blank=True)

    specialized_in = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: Heart Surgery, Angioplasty"
    )

    languages = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: English, Hindi, Malayalam"
    )

    procedures = models.TextField(
        blank=True,
        help_text="Major procedures performed"
    )

    success_rate = models.TextField(
        
        blank=True,
        null=True,
       
    )

    patients_treated = models.TextField(
        blank=True,
        null=True,
        help_text="Total patients treated"
    )

    short_bio = models.TextField(
        blank=True
    )

    full_bio = RichTextUploadingField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def generate_slug(self):
        return self.designation

    
    def clean(self):

       if self.branch and self.specialization:

         if self.specialization.branch_id != self.branch_id:

            raise ValidationError(
                "Selected specialization does not belong to the chosen branch."
            )

    class Meta:
        ordering = ["user__first_name"]

    

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class DoctorEducation(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="educations"
    )

    degree = models.CharField(max_length=255)
    specialization_in = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    year = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
class DoctorCertification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=255)

class DoctorExpertise(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="expertise")
    title = models.CharField(max_length=255)


class DoctorMembership(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="memberships")
    name = models.CharField(max_length=255)
   



class ContentCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ContentType(models.TextChoices):

    BLOG = "blog", "Blog"
    ARTICLE = "article", "Article"
    NEWS = "news", "News"
   


class Content(SEOModel):

    content_type = models.CharField(
        max_length=50,
        choices=ContentType.choices,
        default=ContentType.BLOG
    )

    title = models.CharField(
        max_length=500
    )

    short_description = models.TextField(
        blank=True
    )


    featured_image = models.ImageField(
        upload_to='uploads/contents/featured/',
        blank=True,
        null=True
    )

    hero_banner = models.ImageField(upload_to='uploads/contents/', blank=True, null=True)

    

    content = RichTextUploadingField(
        blank=True
    )

    category = models.ForeignKey(
        "ContentCategory",
        on_delete=models.SET_NULL,
        null=True,
        related_name="contents"
    )

    tags = models.ManyToManyField(
        "Tag",
        blank=True,
        related_name="contents"
    )

    published_by = models.ForeignKey(
        "Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_contents"
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def generate_slug(self):
      return self.title

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
    

class Testimonial(models.Model):

    name = models.CharField(max_length=255)

    designation = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: Patient, CEO, Business Owner"
    )

    image = models.ImageField(
        upload_to="uploads/testimonials/",
        blank=True,
        null=True
    )

    short_description = models.TextField(
        help_text="Customer feedback / testimonial text"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    

class TeamMember(models.Model):

    name = models.CharField(max_length=255)

    designation = models.CharField(
        max_length=255,
        help_text="Example: Doctor, Manager, Staff"
    )

    image = models.ImageField(
        upload_to="uploads/team/",
        blank=True,
        null=True
    )

    short_description = models.TextField(
        blank=True,
        help_text="Short bio or introduction"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ContactPage(models.Model):

    # ✅ ADDRESS
    address = RichTextUploadingField()

    # ✅ PHONE NUMBERS
    phone_primary = models.CharField(
        max_length=20,
        help_text="Main contact number"
    )

    phone_secondary = models.CharField(
        max_length=20,
        blank=True,
        help_text="Optional secondary number"
    )

    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="WhatsApp number"
    )

    # ✅ EMAILS
    email_primary = models.EmailField()

    email_secondary = models.EmailField(
        blank=True
    )

    # ✅ MAP
    map_embed = models.TextField(
        blank=True,
        help_text="Paste Google Maps iframe embed code"
    )

    # ✅ EMERGENCY INFO
    emergency_info = RichTextUploadingField(
        blank=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Contact Page Settings"


    
class PackageCategory(SEOModel):

    # -------------------------
    # BASIC
    # -------------------------
    name = models.CharField(max_length=200)


    Specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name='package_category'
    )

    short_description = models.TextField(blank=True)


    # -------------------------
    # HERO SECTION
    # -------------------------
    hero_title = models.CharField(max_length=255, blank=True)

    hero_description = models.TextField(blank=True)

    hero_banner = models.ImageField(
        upload_to='uploads/packages/',
        blank=True,
        null=True
    )

    hero_banner_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # MAIN SECTION
    # -------------------------
    main_title = models.CharField(max_length=255, blank=True)

    main_description = models.TextField(blank=True)

    main_image = models.ImageField(
        upload_to='uploads/packages/',
        blank=True,
        null=True
    )

    main_image_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # LONG CONTENT
    # -------------------------
    primary_long_description = RichTextUploadingField(blank=True)

    secondary_long_description = RichTextUploadingField(blank=True)

    # -------------------------
    # STATUS
    # -------------------------
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # SLUG
    # -------------------------
    def generate_slug(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Package Category"
        verbose_name_plural = "Package Categories"

    def __str__(self):
        return self.name

class PackageCategoryFAQ(models.Model):

    category = models.ForeignKey(
        PackageCategory,
        on_delete=models.CASCADE,
        related_name="faqs"
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class PackageProduct(models.Model):

    # -------------------------
    # RELATIONSHIP
    # -------------------------
    category = models.ForeignKey(
        PackageCategory,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    featured_image = models.ImageField(
        upload_to='uploads/packages/',
        blank=True,
        null=True
    )

    featured_image_alt = models.CharField(max_length=255, blank=True)

    # -------------------------
    # BASIC INFO
    # -------------------------
    name = models.CharField(max_length=255)

    parameters = models.TextField(
        blank=True,
        help_text="Example: Blood test, ECG, etc."
    )

    # -------------------------
    # PRICING
    # -------------------------
    actual_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    offer_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # -------------------------
    # STATUS
    # -------------------------
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class PackageFeature(models.Model):

    package = models.ForeignKey(
        PackageProduct,
        on_delete=models.CASCADE,
        related_name="features"
    )

    feature = models.CharField(max_length=255)

    def __str__(self):
        return self.feature

class Insurance(models.Model):

    # -------------------------
    # BASIC INFO
    # -------------------------
    name = models.CharField(max_length=200)

    short_description = models.TextField(
        blank=True,
        help_text="Optional short summary"
    )

    long_description = models.TextField(
        blank=True,
        help_text="Optional detailed description"
    )

    # -------------------------
    # MEDIA
    # -------------------------
    featured_image = models.ImageField(
        upload_to='uploads/insurance/',
        blank=True,
        null=True
    )

    featured_image_alt = models.CharField(
        max_length=255,
        blank=True
    )

    # -------------------------
    # STATUS
    # -------------------------
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # -------------------------
    # TIMESTAMP
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   
    # -------------------------
    # META
    # -------------------------
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Insurance"
        verbose_name_plural = "Insurance"

    def __str__(self):
        return self.name

    
class LegalPage(models.Model):

    CONTENT_CHOICES = (
        ('privacy_policy', 'Privacy Policy'),
        ('terms_conditions', 'Terms & Conditions'),
        ('cancellation_policy', 'Cancellation Policy'),
    )

    # -------------------------
    # BASIC
    # -------------------------
    content_type = models.CharField(
        max_length=50,
        choices=CONTENT_CHOICES,
        unique=True
    )

    title = models.CharField(max_length=255)

    content = RichTextUploadingField(
        blank=True,
        help_text="Add full legal content"
    )

    # -------------------------
    # STATUS
    # -------------------------
    is_active = models.BooleanField(default=True)

    # -------------------------
    # TIMESTAMP
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -------------------------
    # META
    # -------------------------
    class Meta:
        ordering = ['content_type']
        verbose_name = "Legal Page"
        verbose_name_plural = "Legal Pages"

    def __str__(self):
        return self.get_content_type_display()


class GlobalSettings(models.Model):

    # -------------------------
    # BRANDING
    # -------------------------
    site_logo = models.ImageField(
        upload_to='uploads/settings/',
        blank=True,
        null=True
    )

    favicon = models.ImageField(
        upload_to='uploads/settings/',
        blank=True,
        null=True
    )

    footer_logo = models.ImageField(
        upload_to='uploads/settings/',
        blank=True,
        null=True
    )

    # -------------------------
    # CONTACT INFO
    # -------------------------
    address = models.TextField(blank=True)

    phone_primary = models.CharField(
        max_length=50,
        blank=True
    )

    phone_secondary = models.CharField(
        max_length=50,
        blank=True
    )

    email_primary = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)

    # -------------------------
    # WHATSAPP
    # -------------------------
    whatsapp_number = models.CharField(
        max_length=50,
        blank=True
    )

    whatsapp_message = models.CharField(
        max_length=255,
        blank=True
    )

    is_whatsapp_enabled = models.BooleanField(default=True)

    # -------------------------
    # FOOTER
    # -------------------------
    footer_description = models.TextField(blank=True)

    copyright_text = models.CharField(
        max_length=255,
        blank=True
    )

    # -------------------------
    # TIMESTAMP
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Global Settings"




class SocialLink(models.Model):

    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('whatsapp', 'WhatsApp'),
        ('other', 'Other'),
    )

    name = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES
    )

    url = models.URLField()

    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: fab fa-facebook-f"
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.get_name_display()



class MenuGroup(models.Model):

    name = models.CharField(max_length=100)  
    slug = models.SlugField(unique=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class MenuItem(models.Model):

    menu = models.ForeignKey(
        MenuGroup,
        on_delete=models.CASCADE,
        related_name="items"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    title = models.CharField(max_length=200)

    url = models.CharField(max_length=255)

    icon_class = models.CharField(max_length=100, blank=True)

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title




# =========================
# MAIN HOMEPAGE MODEL
# =========================
class HomePage(SEOModel):

    # BASIC
    title = models.CharField(max_length=255)

    # ABOUT SECTION
    about_subtitle = models.CharField(max_length=255, blank=True)
    about_title = models.CharField(max_length=255, blank=True)
    about_description = models.TextField(blank=True)

    about_image1 = models.ImageField(upload_to='uploads/home/', blank=True, null=True)
    about_image1_alt = models.CharField(max_length=255, blank=True)

    about_image2 = models.ImageField(upload_to='uploads/home/', blank=True,null=True)
    about_image2_alt = models.CharField(max_length=255, blank=True)

    about_image3 = models.ImageField(upload_to='uploads/home/', blank=True,null=True)
    about_image3_alt = models.CharField(max_length=255, blank=True)

    # SPECIALIZATION
    specialization_subtitle = models.CharField(max_length=255, blank=True)
    specialization_title = models.CharField(max_length=255, blank=True)
    specialization_description = models.TextField(blank=True)

    # STAFF
    staff_title = models.CharField(max_length=255, blank=True)
    staff_subtitle = models.CharField(max_length=255, blank=True)
    staff_description = models.TextField(blank=True)

    # WHY CHOOSE US (MAIN)
    why_choose_title = models.CharField(max_length=255, blank=True)
    why_choose_subtitle = models.CharField(max_length=255, blank=True)
    why_choose_description = models.TextField(blank=True)
    why_choose_banner = models.ImageField(upload_to='uploads/home/', blank=True,null=True)


     # Highlights
    highlights_title = models.CharField(max_length=255, blank=True)
    highlights_subtitle = models.CharField(max_length=255, blank=True)
    highlights_description = models.TextField(blank=True)
   

    # BLOG SECTION
    blog_subtitle = models.CharField(max_length=255, blank=True)
    blog_title = models.CharField(max_length=255, blank=True)
    blog_description = models.TextField(blank=True)

    # ARTICLE SECTION
    article_subtitle = models.CharField(max_length=255, blank=True)
    article_title = models.CharField(max_length=255, blank=True)
    article_description = models.TextField(blank=True)

    # FAQ SECTION
    faq_subtitle = models.CharField(max_length=255, blank=True)
    faq_title = models.CharField(max_length=255, blank=True)
    faq_description = models.TextField(blank=True)

    # TESTIMONIAL
    testimonial_subtitle = models.CharField(max_length=255, blank=True)
    testimonial_title = models.CharField(max_length=255, blank=True)
    testimonial_description = models.TextField(blank=True)

    # PARALLAX / FOOTER CTA
    parallax_subtitle = models.CharField(max_length=255, blank=True)
    parallax_title = models.CharField(max_length=255, blank=True)
    parallax_description = models.TextField(blank=True)
    parallax_cta = models.CharField(max_length=255, blank=True)

    parallax_banner = models.ImageField(upload_to='uploads/home/', blank=True,null=True)

    def __str__(self):
        return self.title



class HomeBanner(models.Model):

    homepage = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="banners"
    )

    title = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    image = models.ImageField(upload_to='uploads/home/banner/', blank=True,null=True)
    image_alt = models.CharField(max_length=255, blank=True)

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class HomeFeature(models.Model):

    homepage = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="features"
    )

    title = models.CharField(max_length=255, blank=True,null=True)
    image = models.ImageField(upload_to='uploads/home/features/', blank=True,null=True)

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class WhyChooseItem(models.Model):

    homepage = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="why_items"
    )

    image = models.ImageField(upload_to='uploads/home/whychoose/', blank=True,null=True)
    title = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class HomeFAQ(models.Model):

    homepage = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="homefaqs"
    )

    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class HighlightItem(models.Model):

    homepage = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="highlight_items"
    )

    image = models.ImageField(
        upload_to='uploads/home/highlights/',
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or "Highlight Item"

    class Meta:
        ordering = ['order']


#============== Doctor Availablity System===================#
class DoctorSchedule(models.Model):

    doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    specialization = models.ForeignKey(
        "Specialization",
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor}"
    


class DoctorScheduleTime(models.Model):

    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    schedule = models.ForeignKey(
        DoctorSchedule,
        on_delete=models.CASCADE,
        related_name="times"
    )

    day_of_week = models.IntegerField(choices=DAY_CHOICES)

    start_time = models.TimeField()
    end_time = models.TimeField()

    slot_duration = models.PositiveIntegerField(default=30)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"



class DoctorLeave(models.Model):

    doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.CASCADE,
        related_name="leaves"
    )

    date = models.DateField()

    is_full_day = models.BooleanField(default=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.doctor} - {self.date}"