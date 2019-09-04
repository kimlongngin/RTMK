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
from datetime import date, datetime, timedelta, time
from django.views.decorators.csrf import csrf_exempt, csrf_protect



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
		today = date.today()
		user = request.user

		invoice_number = increment_invoice_number()
		customer = Customer.objects.filter(is_status=True).order_by('-full_name')
		data = ProductCategory.objects.filter(is_status=True).order_by('-created_at')
		products = Product.objects.filter(is_status=True).order_by('-created_at')  
		today_sale = SaleInvoice.objects.filter(is_status=True, created_at__year=today.year, created_at__month=today.month, created_at__day=today.day)
		
		all_sales = []
		total = 0
		if today_sale:
			for i in today_sale:
				if i.sale_invoice.all():
					for j in i.sale_invoice.all():
						if int(j.discount > 0): 
							sub_total = j.unit * j.unit_price 
							discount = (sub_total * j.discount)/100
							itotal = sub_total - discount
							total = total + itotal
						else:
							sub_total = j.unit * j.unit_price 
							total = total + sub_total

				all_sales.append({"itotal":total, "id":i.id, "invoice_id":i.invoice_number, "user":i.user, "customer":i.customer, "created_at":i.created_at})	
				
		return render(request, self.template_name, {'sale_today':all_sales, 'all_customers':customer, 'all_categories': data, 'all_products':products, 'invoice_number': invoice_number, 'user':user}) 

def filter_category(request):
	if request.is_ajax():
		id = request.GET['myid']
		data = serializers.serialize('json', Product.objects.filter(product_category__id = id, is_status=True).order_by('-created_at') )
		return HttpResponse(data, content_type="application/json")	
	else:
		return HttpResponse("<h1> Welcome !!! </h1>")

def filter_product(request):

	if request.is_ajax():
		key_term = request.GET['key_term']
		data = serializers.serialize('json', Product.objects.filter(name__contains=key_term, is_status=True) | Product.objects.filter(product_number = key_term, is_status=True) | Product.objects.filter(serial_number=key_term, is_status=True))
		return HttpResponse(data, content_type="application/json")
		
	else:
		return HttpResponse("<h1> Welcome !!! </h1>")

def filter_customer(request):

	if request.is_ajax():
		key_term = request.GET['key_term']
		data = serializers.serialize('json', Customer.objects.filter(full_name__contains=key_term,  is_status=True).order_by('full_name') | Customer.objects.filter(email__contains=key_term,  is_status=True).order_by('full_name') | Customer.objects.filter(phone_number__contains=key_term,  is_status=True).order_by('full_name'))
		return HttpResponse(data, content_type="application/json")
		
	else:
		return HttpResponse("<h1> Welcome !!! </h1>")

@csrf_protect
def save_order_product_list(request):

	if request.is_ajax():
		invoice_no = request.GET['invoice_no']
		client_key = request.GET['client_key']
		user = request.user
		sale_product = request.GET['sale_item']

		data_product = json.loads(sale_product)
		
		
		# productObjects.push({"Id":id, "Name":name, "Price": price, "Special_price":special_price, "Unit": Number(1), "Discount": 
		
		try:
			s_customer = Customer.objects.get(pk = client_key)
		except Customer.DoesNotExist:
			# mydata['data'] = 'Customer does not exist!'
			return HttpResponse({'data':'Customer does not exist!'}, content_type="application/json")
		
		try:
			s_invoice = SaleInvoice.objects.get(invoice_number=invoice_no, is_status=True)
		except SaleInvoice.DoesNotExist:
			Binvoice = SaleInvoice(invoice_number = invoice_no, user=user, customer = s_customer, description="Auto save from front end.")
			Binvoice.save()

		n_invoice = SaleInvoice.objects.get(invoice_number=invoice_no, is_status=True)
		if n_invoice:
			for i in data_product:
				p_id = i["Id"]
				try:
					s_product = Product.objects.get(id=p_id, is_status=True)
				except Product.DoesNotExist:
					SaleInvoice.objects.filter(invoice_number=invoice_no).delete()
					return HttpResponse("Product number does not exist")

				p_unit = i["Unit"]
				p_price = i["Price"]
				p_special_price = i["Special_price"]
				p_discount = i["Discount"]
				if s_product:
					if float(p_special_price) > 0:
						b_sale_item = SaleInvoiceItem(invoice=n_invoice, product=s_product, unit=p_unit, unit_price = p_special_price, discount=p_discount, description="Auto save item.")
						b_sale_item.save()
					else:
						b_sale_item = SaleInvoiceItem(invoice=n_invoice, product=s_product, unit=p_unit, unit_price = p_price, discount=p_discount, description="Auto save item.")
						b_sale_item.save() 
		today = date.today()
		today_sale = SaleInvoice.objects.filter(is_status=True, created_at__year=today.year, created_at__month=today.month, created_at__day=today.day)
		
		all_sales = []
		total = 0
		if today_sale:
			for i in today_sale:
				if i.sale_invoice.all():
					for j in i.sale_invoice.all():
						if int(j.discount > 0): 
							sub_total = j.unit * j.unit_price 
							discount = (sub_total * j.discount)/100
							itotal = sub_total - discount
							total = total + itotal
						else:
							sub_total = j.unit * j.unit_price 
							total = total + sub_total
				full_name = i.user.first_name + '' + i.user.last_name
				customer_name = i.customer.full_name
				date_time = str(i.created_at)
				all_sales.append({"itotal":total, "id":i.id, "invoice_id":i.invoice_number, "user":full_name, "customer":customer_name, "created_at": date_time})	
		print(all_sales)

		# data = serializers.serialize('json', {'result': all_sales})
		# print(data)

		return HttpResponse(json.dumps({'result': all_sales}), content_type="application/json")
		
	else:
		return HttpResponse("<h1> Welcome !!! </h1>")

