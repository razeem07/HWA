from django.shortcuts import render, get_object_or_404,redirect,redirect
from administrator.models import Specialization,Redirect,Doctor,Content,AboutPage,TeamMember,Testimonial,ContactPage,Tag,Service,HomePage,LegalPage,Packages,Insurance,Gallery
from .models import ContactSubmission
from django.http import JsonResponse
from utils.schema import specialization_schema,doctor_schema
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponse
from utils.pages import get_listing_page
from django.db.models import Count
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.


def home(request):

    homepage = HomePage.objects.first()  # or use slug if you have one

    banners = homepage.banners.all().order_by('order') if homepage else []

    features = homepage.features.all().order_by('order') if homepage else []

    why_specialization = homepage.why_items.all().order_by('order') if homepage else []

    highlights =homepage.highlight_items.all().order_by('order') if homepage else[]

    doctors = Doctor.objects.filter(
        is_active=True
    ).order_by("-created_at")[:4]

    blogs = Content.objects.filter(
        content_type='blog',
        is_active=True
    ).order_by('-published_at')[:3]

    return render(
        request,
        "pages/index.html",
        {  "homepage": homepage,
         "banners": banners, 
         "features": features,
         "why_specialization": why_specialization,
         "highlights" :highlights,
         "doctors": doctors,
         "blogs": blogs }
    )
    



def about(request):

    page = get_listing_page("about-us")


    breadcrumbs = [
        {"name": "About Us", "url": ""}
    ]

    about = AboutPage.objects.first()

    team_members = TeamMember.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)

    return render(
        request,
        "pages/about.html",
        {"about": about,
         "team_members": team_members,
        "testimonials": testimonials,
          "page": page,
          "seo":page,
          "page_title": page.banner_title if about else "About Us",
          "page_description": page.banner_description,
          "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs,
         }
    )

def contact(request):

    page = get_listing_page("contact")

    breadcrumbs = [
        {"name": "Contact Us", "url": ""}
    ]
  
    contact = ContactPage.objects.first()

    return render(
        request,
        "pages/contact.html",
        {
            "contact": contact,
            "page": page,
            "page_title": page.banner_title if about else "About Us",
          "page_description": page.banner_description,
          "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs,

        }
    )


def contact_submit(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # 🔥 BASIC VALIDATION
        if not name or not email or not subject or not message:
            return JsonResponse({
                "status": "error",
                "message": "Please fill all required fields"
            })

        # 🔥 SAVE TO DB
        ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        return JsonResponse({
            "status": "success",
            "message": "Message sent successfully"
        })

    return JsonResponse({"status": "error"}, status=400)

def blog_list(request):
  
    page = get_listing_page("blog")
    blogs = Content.objects.filter(
        content_type='blog',
        is_active=True
    ).order_by('-published_at')

    query = request.GET.get("q")
    category = request.GET.get("category")
    tag = request.GET.get("tag")

      # 🔥 SEARCH LOGIC
    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    
    # 📂 CATEGORY FILTER
    if category:
        blogs = blogs.filter(category_id=category)

# 🏷 TAG FILTER
    if tag:
          blogs = blogs.filter(tags__id=tag)
    
      # 🔥 Dynamic categories with count
    categories = (
        Content.objects.filter(
            content_type='blog',
            is_active=True
        )
        .values('category__id', 'category__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

       # ✅ TAGS WITH COUNT 🔥
    tags = (
        Tag.objects.filter(
            is_active=True,
            contents__content_type='blog',
            contents__is_active=True
        )
        .annotate(total=Count('contents'))
        .order_by('-total')
    )


      # ✅ RECENT POSTS
    recent_posts = Content.objects.filter(
        content_type='blog',
        is_active=True
    ).order_by('-published_at')[:3]

    breadcrumbs = [
        {"name": "blogs", "url": ""}
    ]

      # 🔥 PAGINATION
    paginator = Paginator(blogs, 10)  # 20 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(
        request,
        "blog/list.html",
        {"blogs": blogs,
           "categories": categories,
             "tags": tags,
              "recent_posts": recent_posts,
               "page": page,
               "page_title": page.banner_title if about else "About Us",
                  "page_description": page.banner_description,
                  "banner_image": page.banner_image if about else None,
                   "breadcrumbs": breadcrumbs,
                   "page_obj":page_obj,
                    "query": query,
                      "category": category,
                        "tag": tag,
                    
          }
    )

def blog_detail(request,slug):
  
    blog = get_object_or_404(
        Content,
        slug=slug,
        content_type='blog',
        is_active=True
    )


      # 🔥 Dynamic categories with count
    categories = (
        Content.objects.filter(
            content_type='blog',
            is_active=True
        )
        .values('category__id', 'category__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

      # 🔥 Related by category
    related_blogs = Content.objects.filter(
        content_type='blog',
        is_active=True,
        category=blog.category
    ).exclude(id=blog.id)

    # 🔥 If tags exist → improve relevance
    if blog.tags.exists():
        related_blogs = related_blogs.filter(
            tags__in=blog.tags.all()
        ).distinct()

    related_blogs = related_blogs.order_by('-published_at')[:3]

    breadcrumbs = [
    {
        "name": "Blogs",
        "url": reverse("userapp:blog_list")
    },
    {
        "name": blog.title,
        "url": ""
    }
]

    return render(
        request,
        "blog/detail.html",
        {"blog": blog,
        "related_blogs": related_blogs,
         "categories": categories,
         "breadcrumbs": breadcrumbs
        }
    )





def specialization_list(request):

    page = get_listing_page("specializations")

    breadcrumbs = [
        {"name": "Specializations", "url": ""}
    ]

    specializations = Specialization.objects.filter(
        is_active=True,
        is_deleted=False
    ).order_by("name")

    return render(
        request,
        "specialization/list.html",
        {"specializations": specializations,
          "page": page,
          "seo":page,
          "page_title": page.banner_title if about else "Specializations",
          "page_description": page.banner_description,
           "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs,
         }
    )


def specialization_detail(request, slug):

    try:
        specialization = Specialization.objects.prefetch_related(
           
            "faqs"
        ).get(slug=slug)

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

    services = specialization.featured_services.filter(
        is_active=True,
        is_deleted=False
    )

    
    # ✅ FILTER ACTIVE DOCTORS
    doctors = specialization.doctors.filter(
        is_active=True,
        is_deleted=False
    )

    breadcrumbs = [
    {
        "name": "Specializations",
        "url": reverse("userapp:specialization_list")
    },
    {
        "name": specialization.name,
        "url": ""
    }
]

    schema = specialization_schema(specialization)

    return render(request, "specialization/detail.html", {
        "specialization": specialization,
        "seo": specialization,
        "schema": schema,
        "doctors": doctors,
        "breadcrumbs": breadcrumbs,
        "services":services,
        "service_count": services.count()
        
    })



def service_detail(request, slug):

    try:
        service = Service.objects.select_related(
            "specialization"
        ).prefetch_related(
            "faqs"
        ).get(slug=slug)

        testimonials = Testimonial.objects.filter(
        is_active=True
    ).order_by('-created_at')

    except Service.DoesNotExist:

        redirect_obj = Redirect.objects.filter(
            model_name="service",
            old_slug=slug
        ).first()

        if redirect_obj:
            return redirect(
                "userapp:service_detail",
                slug=redirect_obj.new_slug,
                permanent=True
            )

        raise
  
  
    return render(request, "service/detail.html", {
        "service": service,
        "seo": service,
        "testimonials":testimonials
    })


def doctor_detail(request, slug):

    try:
        doctor = Doctor.objects.select_related(
            "user",
            "specialization"
        ).prefetch_related(
                 "educations",
                 "certifications",
                 "expertise",
                 "memberships").get(slug=slug)

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
    
    breadcrumbs = [
    {
        "name": "Doctors",
        "url": reverse("userapp:doctor_list")
    },
    {
        "name": doctor.user.first_name,
        "url": ""
    }
    ]
    schema = doctor_schema(doctor)
    return render(
        request,
        "doctors/detail.html",
        {"doctor": doctor,
          "seo" :doctor,
          "schema": schema,
           "breadcrumbs": breadcrumbs
          
          }
    )

def doctor_list(request):

    page = get_listing_page("doctors")

    doctors = Doctor.objects.filter(
        is_active=True
    ).select_related("user","specialization","branch")


    breadcrumbs = [
        {"name": "Specializations", "url": ""}
    ]
    return render(
        request,
        "doctors/list.html",
        {"doctors": doctors,
          "page_title": page.banner_title if about else "Specializations",
          "page_description": page.banner_description,
           "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs}
    )



def get_packages_with_palette(packages):

    PALETTES = [
        {'bg': '#185FA5', 'pill': '#B5D4F4', 'pill_text': '#0C447C', 'btn': '#0C447C'},
        {'bg': '#0F6E56', 'pill': '#9FE1CB', 'pill_text': '#085041', 'btn': '#085041'},
        {'bg': '#993C1D', 'pill': '#F5C4B3', 'pill_text': '#712B13', 'btn': '#712B13'},
        {'bg': '#534AB7', 'pill': '#CECBF6', 'pill_text': '#3C3489', 'btn': '#3C3489'},
        {'bg': '#854F0B', 'pill': '#FAC775', 'pill_text': '#633806', 'btn': '#633806'},
        {'bg': '#993556', 'pill': '#F4C0D1', 'pill_text': '#72243E', 'btn': '#72243E'},
    ]

    return [
        (pkg, PALETTES[i % len(PALETTES)])
        for i, pkg in enumerate(packages)
    ] 

def package_list(request):

    page = get_listing_page("packages")

    breadcrumbs = [
        {"name": "Packages", "url": ""}
    ]

    category_id = request.GET.get('category')

    categories = Specialization.objects.all()

    packages = Packages.objects.filter(is_active=True)

    if category_id:
        packages = packages.filter(Specialization_id=category_id)
    
    packages_with_palette = get_packages_with_palette(packages)

    return render(request, "packages/list.html", {
        "packages": packages,
        "categories": categories,
        "selected_category": category_id,
        "packages_with_palette": packages_with_palette,
         "page_title": page.banner_title if about else "Specializations",
          "page_description": page.banner_description,
           "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs
    })


def package_list_ajax(request):

    specialization_id = request.GET.get('specialization')

    packages = Packages.objects.filter(is_active=True)

    if specialization_id:
        packages = packages.filter(Specialization_id=specialization_id)

    packages_with_palette = get_packages_with_palette(packages)

    html = render_to_string(
        "partials/package_list.html",
        {"packages_with_palette": packages_with_palette}
    )

    return JsonResponse({"html": html})






def insurance_list(request):

    page = get_listing_page("insurance")

    breadcrumbs = [
        {"name": "Insurance", "url": ""}
    ]

   
    insurances = Insurance.objects.filter(
        is_active=True,
        is_deleted=False
    )

    return render(request, "insurance/list.html", {
        "insurances": insurances,
        "page_title": page.banner_title if about else "Specializations",
          "page_description": page.banner_description,
           "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs
    })





def articles_detail(request,slug):

    article = get_object_or_404(
        Content,
        slug=slug,
        content_type='article',
        is_active=True
    )


      # 🔥 Dynamic categories with count
    categories = (
        Content.objects.filter(
            content_type='article',
            is_active=True
        )
        .values('category__id', 'category__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

      # 🔥 Related by category
    related_blogs = Content.objects.filter(
        content_type='article',
        is_active=True,
        category=article.category
    ).exclude(id=article.id)

    # 🔥 If tags exist → improve relevance
    if article.tags.exists():
        related_blogs = related_blogs.filter(
            tags__in=article.tags.all()
        ).distinct()

    related_blogs = related_blogs.order_by('-published_at')[:3]

    return render(
        request,
        "articles/detail.html",
        {"article": article,
        "related_blogs": related_blogs,
         "categories": categories
        }
    )


    

def articles_list(request):

            
    articles = Content.objects.filter(
        content_type='article',
        is_active=True
    ).order_by('-published_at')


    
      # 🔥 Dynamic categories with count
    categories = (
        Content.objects.filter(
            content_type='article',
            is_active=True
        )
        .values('category__id', 'category__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

       # ✅ TAGS WITH COUNT 🔥
    tags = (
        Tag.objects.filter(
            is_active=True,
            contents__content_type='article',
            contents__is_active=True
        )
        .annotate(total=Count('contents'))
        .order_by('-total')
    )

      # ✅ RECENT POSTS
    recent_posts = Content.objects.filter(
        content_type='article',
        is_active=True
    ).order_by('-published_at')[:3]

    

    return render(
        request,
        "articles/list.html",
        {"articles": articles,
           "categories": categories,
             "tags": tags,
              "recent_posts": recent_posts}
    )



def legal_page_detail(request, slug):
    page = get_object_or_404(LegalPage, slug=slug, is_active=True)

    return render(request, "pages/legal_detail.html", {
        "page": page
    })





def gallery_page(request):

    galleries = Gallery.objects.filter(is_active=True).prefetch_related('images')

    return render(request, "pages/gallery.html", {
        "galleries": galleries
    })