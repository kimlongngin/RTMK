from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import HttpResponse
from django.template import loader 
from django.views import generic
from django.urls import reverse_lazy


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View, TemplateView 
from product.models import Product
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserForm, UserLoginForm, RTUserForm
from django.template import loader 
from django.views.generic.list import ListView
from django.contrib import messages


def auth_logout(request):
  logout(request)
  return redirect('usercontrol:login')


# User Login from the browser for the end user 
class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'registration/login.html'
	
	def get(self, request):

		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})	
		
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		username = request.POST['username']
		password = request.POST['password']
	
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('MainView:main_view_index')
		else:
			return render(request, self.template_name, {'form':form})


# User Login from the browser for the end user 



class UserFormView(View):
	form_class = RTUserForm
	template_name = 'registration/registration_form.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})	
		
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False) 
			username = form.cleaned_data['username']  
			data = User.objects.filter(username=username)
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			# return user objects if credentials are corrects 
			user = authenticate(username = username, password = password)
			if user is not None: 
				if user.is_active: 
					login(request, user) 
					return redirect('usercontrol:index') 
		return render(request, self.template_name, {'form':form}) 


class IndexView(generic.ListView):
	template_name =  'index.html'
	context_object_name = 'all_product'
	paginate_by = 3

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)	
		
	def get_queryset(self):
		return Product.objects.filter(is_status=True).order_by('-created_at')


class ListUserView(SuccessMessageMixin, generic.ListView):
	template_name =  'userprofile/list_user.html'
	context_object_name = 'list_user'
	paginate_by = 20

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)	
		
	def get_queryset(self):
		data = User.objects.filter()
		return data




