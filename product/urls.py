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
    path('', views.IndexView.as_view(), name='product_index'),
    path('search/', SearchProductView.as_view(), name='product_search'),
    path('request_rate/', RateView.as_view(), name='request_rate'),
    # path('request_rate/', views.RateView, name='request_rate'),
  	url(r'^product_in_stock/$', views.ProductInStockView.as_view(), name='product_in_stock'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='product_detail'),
    url(r'^category_list/$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^category_product/(?P<pk>[0-9]+)/(?P<cate_name>[0-9, a-z, A-Z]+)/$', views.CategoryProductView.as_view(), name='category_product'),
    url(r'^request_rate_one/$', views.request_rate_one, name='request_rate_one'),
    url(r'^save_order/$', views.SaveOrderView.as_view(), name='save_order'),
    url(r'^save_order_index/$', views.SaveOrderIndexView.as_view(), name='save_order_index'),
    url(r'^list_cart/$', views.ListCartView.as_view(), name='list_cart'),
    url(r'^list_promotion/$', views.PromotionView.as_view(), name='list_promotion'),
    url(r'^search_list_cart/$', views.SearchListCart.as_view(), name='search_list_cart'),
    url(r'^delete_cart/(?P<pk>[0-9]+)/$', views.DeleteCart.as_view(), name='delete_cart'),
    url(r'^delete_cart_search/(?P<pk>[0-9]+)/$', views.DeleteCartSearch.as_view(), name='delete_cart_search'),
    url(r'^avtivation_cart/$', views.avtivation_cart, name='avtivation_cart'),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)