from django.conf.urls import url
from django.urls import path, include
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

from django.contrib.auth import views as auth_views


app_name = 'usercontrol'

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.auth_logout, name='auth_logout' ),
	url(r'^register/$', views.UserFormView.as_view(), name='register'),
	url(r'^usercontrol/', views.IndexView.as_view(), name='index'),
	url(r'^userlist/', views.ListUserView.as_view(), name='listuser'),


	# url(r'^login/$', auth_views.login, name='login'),	
	# url(r'^logout/$', views.auth_logout, name='auth_logout' ),
]
