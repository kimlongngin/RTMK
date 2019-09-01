from django.shortcuts import render, redirect, get_object_or_404, Http404, render_to_response
from django.http import HttpResponse
from django.template import loader 
from django.views import generic
from django.urls import reverse_lazy


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View, TemplateView 
from product.models import Product, ProductInStock, ProductCategory
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ProductSearchForm
from django.template import loader 
from django.views.generic.list import ListView
from django.contrib import messages
from django.http import JsonResponse

from django.core.paginator import Paginator



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
					# Product.save(update_fields=["active"]) 
					ireview = data[0].review
					ireview = ireview + 1
					Product.objects.filter(id = self.kwargs['pk'] ).update(review = ireview)

				return render(request, self.template_name, {'products':data})

			except Product.DoesNotExist:
				raise Http404(" Data does not exist")
		else:
			raise Http404("Please check your data again.")


class SearchProductView(ListView):
	model = Product
	template_name = 'product/result_search.html'
	paginate_by = 100

	

	def get(self, request): 
		q = request.GET['q']
		data = Product.objects.filter(name__contains=q, is_status=True) | Product.objects.filter(product_number = q, is_status=True) | Product.objects.filter(serial_number=q, is_status=True)
		return render(request, self.template_name, {'all_product':data, 'title':q})


class ProductInStockView(SuccessMessageMixin, generic.ListView):

	model = ProductInStock
	template_name = 'product/stock_view.html'
	context_object_name = 'all_product_in_stock'
	paginate_by = 100

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return ProductInStock.objects.filter(is_status=True).order_by('-created_at')


class CategoryListView(SuccessMessageMixin, generic.ListView):
	model = ProductCategory
	template_name = 'product/category_list.html'
	context_object_name = 'all_product_category_ist'
	paginate_by = 100

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return ProductCategory.objects.filter(is_status=True).order_by('-created_at')
		

class CategoryProductView(SuccessMessageMixin, generic.ListView):
		
	model = ProductCategory
	template_name = 'product/category_product.html'
	context_object_name = 'all_product'
	paginate_by = 100

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)


	def get(self, request, *args, **kwargs):

		if self.kwargs['pk']:
			try:
				page_num = 20
				data = Product.objects.filter(product_category=self.kwargs['pk'], is_status=True)
				paginator = Paginator(data, page_num) # Show 25 contacts per page

				page = request.GET.get('page')
				contacts = paginator.get_page(page)

				return render(request, self.template_name, {'all_product':contacts, 'cate_name': self.kwargs['cate_name'], 'paginator_num':page_num, 'all_data':data })

			except Product.DoesNotExist:
				raise Http404(" Data does not exist")
		else:
			raise Http404("Please check your data again.")

	# def get_queryset(self, request, *args, **kwargs):
	# 	return ProductCategory.objects.filter(is_status=True).order_by('-created_at')





	# def get(self, request): 
	# 	data = ProductInStock.objects.filter(is_status=True) 
	# 	return render(request, self.template_name, {'all_product_in_stock':data})
	

# def RateView(request):

# 	if request.method == "POST":
# 		print('loading ajax')
# 		data = request.GET('productID')
# 		print(data)
# 		return HttpResponse(data)


	

	

