"""RTsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path, include
from django.apps import apps
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

"""
    Check data for uploading
"""
from django.conf import settings 
from django.conf.urls.static import static 

app_name = 'RTsite'
admin.site.site_header = "RTMK Admin"
admin.site.site_title = "RTMK Admin Portal"
admin.site.index_title = "Welcome to RTMK product marketing "

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^admin/', include(admin.site.urls)),
    # path('category/', include('category.urls')),
    # path('', include('category.urls')), # login at the page loading. http://127.0.0.1:8000 #
    path('product/', include('product.urls')),
    path('product_history/', include('product_history.urls')),
    path('usercontrol/', include('usercontrol.urls'))
    
    # url(r'^admin/', admin.site.urls),
    # url(r'^category/', views.index, 'category-index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)