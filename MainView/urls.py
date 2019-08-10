from django.conf.urls import include, url
from . import views
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout


app_name = 'MainView'
urlpatterns = [
    url(r'^detail/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='product_detail'),
    url(r'^', views.IndexView.as_view(), name='product_index'),
    url(r'^search/$', views.SearchProductView.as_view(), name='product_search'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
