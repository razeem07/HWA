from django.shortcuts import render, get_object_or_404,redirect,redirect
from administrator.models import Specialization,Redirect,Doctor,Content,AboutPage,TeamMember,Testimonial,ContactPage,Tag,Service,HomePage,LegalPage,Packages,Insurance,Gallery
from .models import ContactSubmission
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.http import url_has_allowed_host_and_scheme
from utils.schema import specialization_schema,doctor_schema
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponse
from utils.pages import get_listing_page
from django.db.models import Count
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib import messages
from .models import NewsletterSubscriber




# Create your views here.


def home(request):

    homepage = HomePage.objects.first()  # or use slug if you have one

    banners = homepage.banners.all().order_by('order') if homepage else []

    features = homepage.features.all().order_by('order') if homepage else []

    why_specialization = homepage.why_items.all().order_by('order') if homepage else []

    highlights =homepage.highlight_items.all().order_by('order') if homepage else[]

    doctors = Doctor.objects.filter(
        is_active=True,
        is_deleted=False
    ).order_by("-created_at")

    blogs = Content.objects.filter(
        content_type='blog',
        is_active=True
    ).order_by('-published_at')[:3]

    return render(
        request,
        "pages/index.html",
        {  "homepage": homepage,
         "seo": homepage,
         "home_faqs": homepage.homefaqs.all().order_by('order') if homepage else [],
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
          "seo": about if about and about.meta_title else page,
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
            "seo": page,
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

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                "status": "error",
                "message": "Please enter a valid email"
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
    if category and category.isdigit():
        blogs = blogs.filter(category_id=category)

# 🏷 TAG FILTER
    if tag and tag.isdigit():
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
    paginator = Paginator(blogs, 20)  # 20 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    return render(
        request,
        "blog/list.html",
        {"blogs": blogs,
           "seo": page,
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

def content_redirect(slug, content_type, url_name):
    """Permanent redirect when a blog/article slug has been changed."""
    if Content.objects.filter(slug=slug, content_type=content_type, is_active=True).exists():
        return None

    redirect_obj = Redirect.objects.filter(
        model_name="content",
        old_slug=slug
    ).order_by("-created_at").first()

    if redirect_obj:
        return redirect(url_name, slug=redirect_obj.new_slug, permanent=True)

    return None


def blog_detail(request,slug):

    moved = content_redirect(slug, "blog", "userapp:blog-detail")
    if moved:
        return moved

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

    query = request.GET.get("q")
    category = request.GET.get("category")
    tag = request.GET.get("tag")

    recent_posts = Content.objects.filter(
    content_type='blog',
    is_active=True
    ).exclude(id=blog.id).order_by('-published_at')[:5]


      # Previous blog (older)
    previous_blog = Content.objects.filter(
    content_type='blog',
    is_active=True,
    published_at__lt=blog.published_at
    ).order_by('-published_at').first()

# Next blog (newer)
    next_blog = Content.objects.filter(
    content_type='blog',
    is_active=True,
    published_at__gt=blog.published_at
     ).order_by('published_at').first()

    return render(
        request,
        "blog/detail.html",
        {"blog": blog,
        "seo": blog,
        "related_blogs": related_blogs,
         "categories": categories,
         "breadcrumbs": breadcrumbs,

          "recent_posts": recent_posts,
        "query": query,
        "category": category,
        "tag": tag,

        "previous_blog": previous_blog,
        "next_blog": next_blog,
      
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
            "footer_title" :page.footer_title,
           "footer_description" :page.footer_description,
            "page_cta" :page.page_cta,
         }
    )


def specialization_detail(request, slug):

    try:
        specialization = Specialization.objects.prefetch_related(
           
            "faqs"
        ).get(slug=slug, is_active=True, is_deleted=False)

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

        raise Http404

    services = specialization.featured_services.filter(
        is_active=True,
        is_deleted=False
    )

    
    # ✅ FILTER ACTIVE DOCTORS
    doctors = Doctor.in_department(specialization.pk).filter(
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
    
    page = get_listing_page("specializations")

    schema = specialization_schema(specialization)

    return render(request, "specialization/detail.html", {
        "specialization": specialization,
        "seo": specialization,
        "schema": schema,
        "doctors": doctors,
        "breadcrumbs": breadcrumbs,
        "services":services,
        "service_count": services.count(),
        "footer_title" :page.footer_title,
           "footer_description" :page.footer_description,
            "page_cta" :page.page_cta,
        
    })



def service_detail(request, slug):

    try:
        service = Service.objects.select_related(
            "specialization"
        ).prefetch_related(
            "faqs"
        ).get(slug=slug, is_active=True, is_deleted=False)

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

        raise Http404

    page = get_listing_page("services")
  
  
    return render(request, "service/detail.html", {
        "service": service,
        "seo": service,
        "testimonials":testimonials,
         "footer_title" :page.footer_title,
           "footer_description" :page.footer_description,
            "page_cta" :page.page_cta,
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
                 "memberships").get(slug=slug, is_active=True, is_deleted=False)

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

        raise Http404
    page = get_listing_page("doctors")
    
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
           "breadcrumbs": breadcrumbs,
           "footer_title" :page.footer_title,
           "footer_description" :page.footer_description,
            "page_cta" :page.page_cta,
          
          }
    )

def doctor_list(request):

    query = request.GET.get("q")
    specialization = request.GET.get("specialization")

    page = get_listing_page("doctors")

    doctors = Doctor.objects.filter(
        is_active=True
    ).select_related("user","specialization","branch")
    

    if query:
        doctors = doctors.annotate(
        full_name=Concat('user__first_name', Value(' '), 'user__last_name')
    ).filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(full_name__icontains=query) |   # 🔥 THIS FIXES IT
        Q(specialization__name__icontains=query) |
        Q(additional_specializations__name__icontains=query)
    ).distinct()
    # 📂 SPECIALIZATION FILTER
    if specialization and specialization.isdigit():
        doctors = doctors.filter(
            Q(specialization_id=specialization) |
            Q(additional_specializations=specialization)
        ).distinct()

    

    breadcrumbs = [
        {"name": "Doctor", "url": ""}
    ]
    return render(
        request,
        "doctors/list.html",
        {"doctors": doctors,
          "seo": page,
          "page_title": page.banner_title if about else "Specializations",
          "page_description": page.banner_description,
           "banner_image": page.banner_image if about else None,
           "footer_title" :page.footer_title,
           "footer_description" :page.footer_description,
            "page_cta" :page.page_cta,
          "breadcrumbs": breadcrumbs,
            "specialization": specialization,
        "specializations": Specialization.objects.filter(is_active=True, is_deleted=False),
          "query":query,
          
          }
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

    categories = Specialization.objects.filter(is_active=True, is_deleted=False)

    packages = Packages.objects.filter(is_active=True)

    if category_id and category_id.isdigit():
        packages = packages.filter(Specialization_id=category_id)
    
    packages_with_palette = get_packages_with_palette(packages)

    return render(request, "packages/list.html", {
        "packages": packages,
        "seo": page,
        "categories": categories,
        "selected_category": category_id,
        "packages_with_palette": packages_with_palette,
         "page_title": page.banner_title if about else "Specializations",
          "page_description": page.banner_description,
           "footer_title" :page.footer_title,
           "footer_description" :page.footer_description,
            "page_cta" :page.page_cta,
           "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs
    })


def package_list_ajax(request):

    specialization_id = request.GET.get('specialization')

    packages = Packages.objects.filter(is_active=True)

    if specialization_id and specialization_id.isdigit():
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
        "seo": page,
        "page_title": page.banner_title if about else "Specializations",
          "page_description": page.banner_description,
           "banner_image": page.banner_image if about else None,
          "breadcrumbs": breadcrumbs,
           "footer_title" :page.footer_title,
           "footer_description" :page.footer_description,
            "page_cta" :page.page_cta,
    })





def articles_detail(request,slug):

    moved = content_redirect(slug, "article", "userapp:articles_detail")
    if moved:
        return moved

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

    breadcrumbs = [
    {
        "name": "Article",
        "url": reverse("userapp:articles_list")
    },
    {
        "name": article.title,
        "url": ""
    }
   ]

   
    query = request.GET.get("q")
    category = request.GET.get("category")
    tag = request.GET.get("tag")
    
         # Previous blog (older)
    previous_blog = Content.objects.filter(
    content_type='article',
    is_active=True,
    published_at__lt=article.published_at
    ).order_by('-published_at').first()

# Next blog (newer)
    next_blog = Content.objects.filter(
    content_type='article',
    is_active=True,
    published_at__gt=article.published_at
     ).order_by('published_at').first()

    return render(
        request,
        "articles/detail.html",
        {"article": article,
        "seo": article,
        "related_blogs": related_blogs,
         "categories": categories,
         "breadcrumbs" :breadcrumbs,
         "query":query,
         "category":category,
         "tag":tag,
         "previous_blog": previous_blog,
        "next_blog": next_blog,
        }
    )


    

def articles_list(request):

            
    articles = Content.objects.filter(
        content_type='article',
        is_active=True
    ).order_by('-published_at')
     
    breadcrumbs = [
        {"name": "articles", "url": ""}
    ]
    


    
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

     
      # 🔥 PAGINATION
    paginator = Paginator(articles, 10)  # 20 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query = request.GET.get("q")
    category = request.GET.get("category")
    tag = request.GET.get("tag")

    

    return render(
        request,
        "articles/list.html",
        {"articles": articles,
           "seo": get_listing_page("articles"),
           "categories": categories,
             "tags": tags,
              "recent_posts": recent_posts,
              "page_obj":page_obj,
               "breadcrumbs" :breadcrumbs,
               "query":query,
               "category":category,
               "tag":tag,
              }
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




def subscribe_newsletter(request):
    back = request.META.get("HTTP_REFERER")
    if not url_has_allowed_host_and_scheme(back, allowed_hosts={request.get_host()}):
        back = "/"

    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email")
            return redirect(back)

        if NewsletterSubscriber.objects.filter(email=email).exists():
            messages.warning(request, "Already subscribed")
        else:
            NewsletterSubscriber.objects.create(email=email)
            messages.success(request, "Subscribed successfully!")

    return redirect(back)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /administrator/",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /ckeditor/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def sitemap_xml(request):
    paths = ["/", "/about/", "/contact/", "/doctors/", "/specializations/", "/packages/", "/insurance/", "/blogs/", "/articles/", "/gallery/"]
    paths += [f"/specializations/{s}/" for s in Specialization.objects.filter(is_active=True, is_deleted=False).values_list("slug", flat=True)]
    paths += [f"/service/{s}/" for s in Service.objects.filter(is_active=True, is_deleted=False).values_list("slug", flat=True)]
    paths += [f"/doctors/{s}/" for s in Doctor.objects.filter(is_active=True, is_deleted=False).values_list("slug", flat=True)]
    paths += [f"/blogs/{s}/" for s in Content.objects.filter(content_type="blog", is_active=True).values_list("slug", flat=True)]
    paths += [f"/articles/{s}/" for s in Content.objects.filter(content_type="article", is_active=True).values_list("slug", flat=True)]
    paths += [f"/legal/{s}/" for s in LegalPage.objects.filter(is_active=True).values_list("slug", flat=True)]
    urls = "".join(f"<url><loc>{request.build_absolute_uri(p)}</loc></url>" for p in paths)
    return HttpResponse(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
        content_type="application/xml",
    )
