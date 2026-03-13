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



class Redirect(models.Model):

    model_name = models.CharField(max_length=50, blank=True)

    old_slug = models.SlugField()
    new_slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.old_slug} → {self.new_slug}"




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
    main_description = models.TextField(blank=True)

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