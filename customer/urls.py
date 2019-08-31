from django.conf.urls import include, url
from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

app_name = 'customer'

urlpatterns = [
    path('', views.IndexView.as_view(), name='customer_index'),
    url(r'^detail/(?P<full_name>[0-9, a-z, A-Z]+)/', views.CustomerDetailView.as_view(), name='customer_detail'),
    url(r'^list_invoice_detail/(?P<pk>[0-9]+)/(?P<invoice_no>[0-9, a-z, A-Z]+)/(?P<phone_number>[0-9, a-z, A-Z]+)/(?P<address>[0-9, a-z, A-Z]+)/(?P<full_name>[0-9, a-z, A-Z]+)/', views.ListInvoiceDetailView.as_view(), name='list_invoice_detail'),
    
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)