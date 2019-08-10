from django.shortcuts import render, redirect, get_object_or_404, Http404, render_to_response
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
from .forms import ProductSearchForm
from django.template import loader 
from django.views.generic.list import ListView
from django.contrib import messages
from django.http import JsonResponse



class RateView(View):
	def get(self, request):
		print("create")
		print('loading ajax')
		data = request.GET('productID')
		print(data)
		return HttpResponse(data)

class IndexView(SuccessMessageMixin, generic.ListView):
	template_name =  'product/index.html'
	context_object_name = 'all_product'
	paginate_by = 20
	def get_queryset(self):
		return Product.objects.filter(is_status=True).order_by('-created_at')

class DetailView(generic.DetailView):
	template_name =  'product/detail.html'

	def get(self, request, *args, **kwargs):
		# print(self.kwargs['pk'])
		
		if self.kwargs['pk']:
			try:
				data = Product.objects.filter(id=self.kwargs['pk'], is_status=True)
				if data:
					print(data)
					print("hello world")
					# Product.save(update_fields=["active"]) 
					ireview = data[0].review
					ireview = ireview + 1
					Product.objects.update(review = ireview)

				return render(request, self.template_name, {'products':data})

			except Product.DoesNotExist:
				raise Http404(" Data does not exist")
		else:
			raise Http404("Please check your data again.")


class SearchProductView(ListView):
	model = Product
	template_name = 'product/result_search.html'
	paginate_by = 20

	def get(self, request): 
		q = request.GET['q']

		data = Product.objects.filter(name__contains=q, is_status=True) | Product.objects.filter(product_number = q, is_status=True) | Product.objects.filter(serial_number=q, is_status=True)
		return render(request, self.template_name, {'all_product':data, 'title':q})



	

# def RateView(request):

# 	if request.method == "POST":
# 		print('loading ajax')
# 		data = request.GET('productID')
# 		print(data)
# 		return HttpResponse(data)


	

	

