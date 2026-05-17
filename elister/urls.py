"""
URL configuration for elister project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userapp.urls',namespace='userapp')),
    path('administrator/', include('administrator.urls',namespace='administrator')),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('appointment/', include('booking.urls',namespace='appointment')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Append media file routing for local development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Fallback routing to force Gunicorn to serve static assets when running inside Podman
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
else:
    # If DEBUG=True but running under Gunicorn, this catches the standard static prefix
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)