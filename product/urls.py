from django.conf.urls import include, url
from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout


from .views import SearchProductView, RateView

app_name = 'product'

urlpatterns = [
    # path('', views.index, name='product-index'),
    path('search/', SearchProductView.as_view(), name='product_search'),
    path('request_rate/', RateView.as_view(), name='request_rate'),
    # path('request_rate/', views.RateView, name='request_rate'),
  
  	url(r'^product_in_stock/', views.ProductInStockView.as_view(), name='product_in_stock'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='product_detail'),
    url(r'^', views.IndexView.as_view(), name='product_index'),

 
    # url(r'^request_rate/$', views.RateView.as_view(), name='request_rate'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)