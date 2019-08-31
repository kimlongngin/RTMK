from django.conf.urls import include, url
from . import views
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout


app_name = 'sell'
urlpatterns = [
    url(r'^$', views.SaleView.as_view(), name='sale_view'),
   	url(r'^filter_category/$', views.filter_category, name='filter_category'),
   
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)