from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import HttpResponse, JsonResponse
from django.template import loader 
from django.views import generic
from django.urls import reverse_lazy


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View, TemplateView 
from product.models import Product, Promotion, ProductCategory
from customer.models import Customer, SaleInvoiceItem, Payment, SaleInvoice

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.template import loader 
from django.views.generic.list import ListView
from django.contrib import messages
from django.core.paginator import Paginator
from django.core import serializers
import json


def increment_invoice_number():
	last_invoice = SaleInvoice.objects.all().order_by('id').last()
	if not last_invoice:
		return 'INV000001'
	width = 6
	invoice_number = last_invoice.invoice_number
	invoice_int = int(invoice_number.split('INV')[-1])

	new_invoice_int = invoice_int + 1
	formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
	new_invoice_int = 'INV' + str(formatted)
	return str(new_invoice_int)


class SaleView(SuccessMessageMixin, generic.ListView):
	template_name = 'sell/sale.html'
	context_object_name = 'all_categories'
	paginate_by = 100

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)
		
	def get(self, request, *args, **kwargs):
		user = request.user

		invoice_number = increment_invoice_number()
		data = ProductCategory.objects.filter(is_status=True).order_by('-created_at')
		products = Product.objects.filter(is_status=True).order_by('-created_at')  
		return render(request, self.template_name, {'all_categories': data, 'all_products':products, 'invoice_number': invoice_number, 'user':user}) 

def filter_category(request):
	if request.is_ajax():
		id = request.GET['myid']
		
		data = serializers.serialize('json', Product.objects.filter(product_category__id = id, is_status=True).order_by('-created_at') )
		return HttpResponse(data, content_type="application/json")
		
	else:
		return HttpResponse("<h1> Welcome !!! </h1>")
		


