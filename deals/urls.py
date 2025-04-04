"""deals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("edudealio.urls")),
    path('',include("products.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'edudealio.errors_views.custom_404'
handler500 = 'edudealio.errors_views.custom_500'
handler504 = 'edudealio.errors_views.custom_504'
handler403 = 'edudealio.errors_views.custom_403'
handler401 = 'edudealio.errors_views.custom_401'
handler502 = 'edudealio.errors_views.custom_502'
handler503 = 'edudealio.errors_views.custom_503'
handler400 = 'edudealio.errors_views.custom_400'