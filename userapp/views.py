from django.shortcuts import render, get_object_or_404,redirect,redirect
from administrator.models import Specialization,Redirect,Doctor
from utils.schema import specialization_schema,doctor_schema
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponse


# Create your views here.


def home(request):

   
    doctors = Doctor.objects.filter(
        is_active=True
    ).order_by("-created_at")[:4]

    return render(
        request,
        "pages/index.html",
        {"doctors": doctors}
    )
    

def about(request):
  
    return render(request, "pages/about.html")



def contact(request):
  
    return render(request, "pages/contact.html")


def blog_list(request):
  
    return render(request, "blog/list.html")

def blog_detail(request):
  
    return render(request, "blog/detail.html")





def specialization_list(request):

    specializations = Specialization.objects.filter(
        is_active=True,
        is_deleted=False
    ).order_by("name")

    return render(
        request,
        "specialization/list.html",
        {"specializations": specializations}
    )


def specialization_detail(request, slug):

    try:
        specialization = Specialization.objects.get(slug=slug)

    except Specialization.DoesNotExist:

        redirect_obj = Redirect.objects.filter(
            model_name="specialization",
            old_slug=slug
        ).first()

        if redirect_obj:
            return redirect(
                "userapp:specialization_detail",
                slug=redirect_obj.new_slug,
                permanent=True
            )

        raise

    schema = specialization_schema(specialization)

    return render(request, "specialization/detail.html", {
        "specialization": specialization,
        "seo": specialization,
        "schema": schema
    })



def doctor_detail(request, slug):

    try:
        doctor = Doctor.objects.select_related(
            "user",
            "specialization"
        ).get(slug=slug)

    except Doctor.DoesNotExist:

        redirect_obj = Redirect.objects.filter(
            model_name="doctor",
            old_slug=slug
        ).first()

        if redirect_obj:
            return redirect(
                "userapp:doctor_detail",
                slug=redirect_obj.new_slug,
                permanent=True
            )

        raise
    schema = doctor_schema(doctor)
    return render(
        request,
        "doctors/detail.html",
        {"doctor": doctor,
          "seo" :doctor,
          "schema": schema}
    )

def doctor_list(request):

    doctors = Doctor.objects.filter(
        is_active=True
    ).select_related("user","specialization","branch")

    return render(
        request,
        "doctors/list.html",
        {"doctors": doctors}
    )

   


def package_detail(request):

      return render(request, "packages/detail.html")


def package_list(request):

      return render(request, "packages/list.html")



def insurance_detail(request):

      return render(request, "insurance/detail.html")


def insurance_list(request):

      return render(request, "insurance/list.html")



def articles_detail(request):

      return render(request, "articles/detail.html")


def articles_list(request):

      return render(request, "articles/list.html")