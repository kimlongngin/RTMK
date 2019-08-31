from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.http import HttpResponse
from django.template import loader 
from django.views import generic
from django.urls import reverse_lazy


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View, TemplateView 
from product.models import Product, Promotion, ProductCategory
from customer.models import Customer, SaleInvoiceItem, Payment

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.template import loader 
from django.views.generic.list import ListView
from django.contrib import messages
from django.core.paginator import Paginator


class IndexView(SuccessMessageMixin, generic.ListView):
	template_name = 'customer/index.html'
	context_object_name = 'all_customer'
	paginate_by = 100

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)
		
	def get_queryset(self):
		return Customer.objects.filter(is_status=True).order_by('-created_at')
	

class CustomerDetailView(SuccessMessageMixin, generic.ListView):
	template_name = 'customer/detail.html'
	context_object_name = 'detail_customers'
	paginate_by = 100

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):

		if self.kwargs['full_name']:
			try:
				page_num = 100
				data = Customer.objects.filter(full_name=self.kwargs['full_name'], is_status=True)
				paginator = Paginator(data, page_num) # Show 25 contacts per page

				page = request.GET.get('page')
				contacts = paginator.get_page(page)

				return render(request, self.template_name, {'all_invoices':contacts, 'name': self.kwargs['full_name'], 'paginator_num':page_num, 'all_data':data })

			except Customer.DoesNotExist:
				raise Http404(" Data does not exist")
		else:
			raise Http404("Please check your data again.")


class ListInvoiceDetailView(SuccessMessageMixin, generic.ListView):
	template_name = 'customer/list_invoice_detail.html'
	context_object_name = 'list_invoices'
	paginate_by = 100

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):

		phone_number = self.kwargs['phone_number']
		address = self.kwargs['address']

		if self.kwargs['invoice_no']:
			try:
				# Select related field between SaleInvoice with SaleInvoiceItem by "invoice and invoice_number"
				data = SaleInvoiceItem.objects.filter(invoice__invoice_number=self.kwargs['invoice_no'], is_status=True)
				if data:
					grand_total = 0
					for i in data:
						if i.unit_price > 0:
							total = i.unit_price * i.unit
							grand_total = grand_total + total
						else:
							total = i.product.price * i.unit
							grand_total = grand_total + total

				pays = Payment.objects.filter(invoice__invoice_number=self.kwargs['invoice_no'], is_status=True)
				
				total_pay = 0
				if pays:
					for p in pays:
						total_pay = total_pay + p.pay_amount

				equally = grand_total - total_pay

				return render(request, self.template_name, {'equally':equally, 'pays':total_pay, 'full_name':self.kwargs['full_name'], 'grand_total': grand_total, 'list_invoices':data, 'invoice_no':self.kwargs['invoice_no'], 'phone_number':phone_number , 'address':address})
			except SaleInvoiceItem.DoesNotExist:
				raise Http404(" Data does not exist")
		else:
			raise Http404("Please check your data again.")






