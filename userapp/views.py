from django.shortcuts import render, get_object_or_404,redirect,redirect
from administrator.models import Specialization,Redirect
from utils.schema import specialization_schema
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponse


# Create your views here.


def home(request):
    return HttpResponse("Hospital Website – Home Page (Test)")



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

        redirect_obj = Redirect.objects.filter(old_slug=slug).first()

        if redirect_obj:
            return redirect(
                f"/specializations/{redirect_obj.new_slug}/",
                permanent=True
            )

        raise Http404()


    specialization = get_object_or_404(
        Specialization,
        slug=slug,
        is_active=True,
        is_deleted=False
    )

    schema = specialization_schema(specialization)

    return render(request, "specialization/detail.html", {
        "specialization": specialization,
        "seo": specialization,
        "schema": schema
    })