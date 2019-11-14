from django.shortcuts import render, redirect, get_object_or_404, Http404, render_to_response
from django.http import HttpResponse
from django.template import loader 
from django.views import generic
from django.urls import reverse_lazy


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.views.generic import View, TemplateView 
from product.models import Media, Product, ProductInStock, ProductCategory, Rate, ProductCategory, OrderProduct, Promotion
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView 

from .forms import ProductSearchForm
from django.template import loader 
from django.views.generic.list import ListView
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
import json

from django.db.models import Q

from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.contrib import messages


def base_media(request):
	data = Media.objects.filter(is_status=True)
	return {'all_media': data}


def request_rate_one(request):

	if request.is_ajax():

		nid = request.GET['id']
		n_rate = request.GET['n_rate']

		try:
			products = Product.objects.get(id = nid, is_status=True)
			b_rate = Rate(product=products, rate_number=n_rate, rate=n_rate)
			b_rate.save()
		except Product.DoesNotExist as e:
			print(e)
			return HttpResponse('<h4><code>This product not exist in database.</code></h4>')
		
		data = Rate.objects.filter(product=products, is_status=True)
		objs = serializers.serialize('json', data)
		return HttpResponse(objs, content_type="application/json")

	else:
		return HttpResponse('<h4> Not found data. </h4>')


class RateView(View):
	def get(self, request):
		data = request.GET('productID')
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

		# (5*252 + 4*124 + 3*40 + 2*29 + 1*33) / (252+124+40+29+33) = 4.11 and change
		
		rate_1 = 0
		rate_2 = 0
		rate_3 = 0
		rate_4 = 0
		rate_5 = 0
		if self.kwargs['pk']:
			try:
				data = Product.objects.get(id=self.kwargs['pk'], is_status=True)

				cat_id = data.product_category
				re_data = Product.objects.filter(~Q(id=self.kwargs['pk']), product_category=cat_id, is_status=True).order_by('-created_at')[:8]

				if data:
					ireview = data.review
					ireview = ireview + 1
					Product.objects.filter(id = self.kwargs['pk'] ).update(review = ireview)

					d_rate = Rate.objects.filter(product=data)
					for i in d_rate: 
						if i.rate_number == 1.0:
							rate_1 = rate_1 + 1
						elif i.rate_number == 2.0:
							rate_2 = rate_2 + 1
						elif i.rate_number == 3.0:
							rate_3 = rate_3 + 1
						elif i.rate_number == 4.0:
							rate_4 = rate_4 + 1
						else:
							rate_5 = rate_5 + 1


					rates = (5*rate_5 + 4*rate_4 + 3*rate_3 + 2*rate_2 + 1*rate_1) / (rate_5+rate_4+rate_3+rate_2+rate_1)
					rates = round(rates)
				
				order_count = OrderProduct.objects.filter(product=data.id, is_status=True).count()
				
				return render(request, self.template_name, {'all_rate':rates, 'product':data, 'all_redata':re_data, 'order_count': order_count, 'ipk':self.kwargs['pk']})

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
		data = Product.objects.filter(name__contains=q.strip(), is_status=True) | Product.objects.filter(product_number = q.strip(), is_status=True) | Product.objects.filter(serial_number=q.strip(), is_status=True)
		return render(request, self.template_name, {'all_product':data, 'title':q})


class ProductInStockView(SuccessMessageMixin, generic.ListView):

	model = ProductInStock
	template_name = 'product/stock_view.html'
	context_object_name = 'all_product_in_stock'
	paginate_by = 300

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	def get(self, request):

		user = request.user
		products = Product.objects.filter(is_status=True).order_by('-created_at')  
	
		all_product_stock = []
		product_stock = 0
		total_product_sale = 0
		product_left = 0

		if products:
			for i in products:
				product_stock = 0
				total_product_sale = 0
				product_left = 0
				sub_product_amount = 0
				iunit = 0

				if i.product_in_stock.all():
					# check product in stock
					for p in i.product_in_stock.all():
						
						if p.unit > 0:
							product_stock = product_stock + (p.unit *i.product_type.amount) + p.amount 
							iunit = iunit + p.unit
						else:
							product_stock = product_stock + p.amount

						sub_product_amount = sub_product_amount + p.amount

				if i.sale_invoice_item_product.all():

					for item in i.sale_invoice_item_product.all():
						total_product_sale = total_product_sale + item.unit
					product_left = product_stock - total_product_sale # calculate product that sale in saleproductitem model
				
					all_product_stock.append({'product_code': i.product_number, 'id':i.id, 'name':i.name, 'product_type':i.product_type, 'sub_amount':sub_product_amount, 'product_per_amount':i.product_type.amount, 'iunit':iunit, 'unit':total_product_sale, 'total_product':product_left, 'default_image':i.default_image, 'price': i.price, 'special_price':i.special_price })
				
				else:
				
					if product_stock > 0:
						all_product_stock.append({'product_code': i.product_number,'id':i.id, 'name':i.name, 'product_type':i.product_type, 'sub_amount':sub_product_amount, 'product_per_amount':i.product_type.amount, 'iunit':iunit, 'unit':total_product_sale, 'total_product':product_stock, 'default_image':i.default_image, 'price': i.price, 'special_price':i.special_price })
					else:
						all_product_stock.append({'product_code': i.product_number,'id':i.id, 'name':i.name, 'product_type':i.product_type, 'sub_amount':sub_product_amount, 'product_per_amount':i.product_type.amount, 'iunit':iunit, 'unit':total_product_sale, 'total_product':0, 'default_image':i.default_image, 'price': i.price, 'special_price':i.special_price })
		
		return render(request, self.template_name, {'all_product_in_stock':all_product_stock})


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

class SaveOrderView(SuccessMessageMixin, View):

	template_name =  'product/detail.html'
	context_object_name = 'all_product'
	paginate_by = 100
	success_message = "Order successfully !"

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	@method_decorator(login_required(''))
	def post(self, request, *args, **kwargs):
		success_message = "Pay successfully."

		if request.method == 'POST':

			price = request.POST.get('price')
			product_id = request.POST.get('id_product_id')
			client_name = request.POST.get('id_name')
			id_phone_number = request.POST.get('id_phone_number')
			id_email = request.POST.get('id_email')
			id_quantity = request.POST.get('id_quantity')
			id_address = request.POST.get('id_address')

			try:
				product_n = Product.objects.get(id=product_id, is_status=True)

				b_order_product= OrderProduct(product = product_n, customer_name=client_name, phone_number=id_phone_number, email=id_email, quantity=id_quantity, price=price, address=id_address)
				b_order_product.save()

				data = Product.objects.get(id=product_id, is_status=True)
				cat_id = data.product_category
				re_data = Product.objects.filter(~Q(id=product_id), product_category=cat_id, is_status=True).order_by('-created_at')[:8]
				if data:
					ireview = data.review
					ireview = ireview + 1
					Product.objects.filter(id = product_id ).update(review = ireview)

				order_count = OrderProduct.objects.filter(product__order_product=product_id, is_status=True).count()
				
				messages.add_message(request, messages.SUCCESS, "Save successfully.")
			
				return redirect('/detail/'+str(product_id))  
				
				#  return render(request, 'product/detail.html/'+str(product_id), {'messages':success_message})  
				


			except Product.DoesNotExist:
				return HttpResponse('<h3> This product not exist in stock. </h3>')


			return HttpResponse('<h3> Save success. </h3>')

		else:
			return HttpResponse('<div style="text-alight:center;"><h4><code> Invalid form. </code></h4></div>')
				
class SaveOrderIndexView(SuccessMessageMixin, View):

	template_name =  'product/index.html'
	context_object_name = 'all_product'
	paginate_by = 100
	success_message = "Order successfully !"

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	@method_decorator(login_required(''))
	def post(self, request, *args, **kwargs):
		success_message = "Pay successfully."

		if request.method == 'POST':

			price = request.POST.get('price')
			product_id = request.POST.get('id_product_id')
			client_name = request.POST.get('id_name')
			id_phone_number = request.POST.get('id_phone_number')
			id_email = request.POST.get('id_email')
			id_quantity = request.POST.get('id_quantity')
			id_address = request.POST.get('id_address')

			try:
				product_n = Product.objects.get(id=product_id, is_status=True)

				b_order_product= OrderProduct(product = product_n, customer_name=client_name, phone_number=id_phone_number, email=id_email, quantity=id_quantity, price=price, address=id_address)
				b_order_product.save()

				data = Product.objects.get(id=product_id, is_status=True)
				cat_id = data.product_category
				re_data = Product.objects.filter(~Q(id=product_id), product_category=cat_id, is_status=True).order_by('-created_at')[:8]
				if data:
					ireview = data.review
					ireview = ireview + 1
					Product.objects.filter(id = product_id ).update(review = ireview)

				order_count = OrderProduct.objects.filter(product__order_product=product_id, is_status=True).count()
				
				messages.add_message(request, messages.SUCCESS, "Save successfully.")
			
				return redirect('/')  
				
				

			except Product.DoesNotExist:
				return HttpResponse('<h3> This product not exist in stock. </h3>')


			return HttpResponse('<h3> Save success. </h3>')

		else:
			return HttpResponse('<div style="text-alight:center;"><h4><code> Invalid form. </code></h4></div>')
		

class ListCartView(ListView): 
	template_name =  'product/cart.html'
	context_object_name = 'all_cart'
	success_message = "Order successfully !"
	paginate_by = 50

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		data = OrderProduct.objects.filter(is_status=True).order_by('-created_at')
		return data


from datetime import date
class PromotionView(generic.ListView):
	template_name =  'product/promotion.html'
	context_object_name = 'all_product'
	success_message = "Order successfully !"
	paginate_by = 10
	
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		
		itoday = date.today()
		data = Promotion.objects.filter(is_status=True, start_date__date__lte = itoday, end_date__date__gte = itoday)
		# data = Promotion.objects.filter(is_status=True).order_by('-created_at')
		return data


class SearchListCart(generic.ListView): 
	model = OrderProduct
	template_name = 'product/cart_list.html'
	context_object_name = 'all_cart'
	paginate_by = 50
	
	

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)
	

	def get_queryset(self):

		month = [{'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12' }]

		q = self.request.GET['q']
		f_date = self.request.GET['start_date']
		s_date = self.request.GET['end_date']

		#  Check date formate
		fd = f_date.split()
		ed = s_date.split()
		if len(fd) > 1 and len(ed) >1:
			s_d = fd[0]
			s_m = fd[1]
			s_y = fd[2]

			for i in month:
				s_m = i[str(s_m)]

			e_d = ed[0]
			e_m = ed[1]
			e_y = ed[2]

			for i in month:
				e_m = i[str(e_m)]
			is_date = s_y+'-'+s_m+'-'+s_d
			ie_date = e_y+'-'+e_m+'-'+e_d

			if q:
				data = OrderProduct.objects.filter(invoice_number__contains=q.strip()).order_by('-created_at') | OrderProduct.objects.filter(product__contains=q.strip(), created_at__range=(is_date, ie_date)).order_by('-created_at')  | OrderProduct.objects.filter(customer_name__contains=q.strip(), created_at__range=(is_date, ie_date)).order_by('-created_at') | OrderProduct.objects.filter(phone_number__contains=q.strip(), created_at__range=(is_date, ie_date)).order_by('-created_at')
				return data
			else:

				data = OrderProduct.objects.filter(created_at__range=(is_date, ie_date)).order_by('-created_at') 
				return data
		else:
			if q:
				data = OrderProduct.objects.filter(invoice_number__contains=q.strip()).order_by('-created_at') | OrderProduct.objects.filter(customer_name__contains=q.strip()) | OrderProduct.objects.filter(email__contains=q.strip()) | OrderProduct.objects.filter(phone_number__contains=q.strip()).order_by('-created_at')
				return data
			else:
				data = OrderProduct.objects.filter().order_by('-created_at') 
				return data


class DeleteCart(SuccessMessageMixin, DeleteView):
		
	model = OrderProduct 
	success_message = " Deleted successfully!"
	success_url = reverse_lazy('product:list_cart')
	template_name = 'product/delete_cart.html'

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	@method_decorator(login_required(''))
	def get(self, request, *args, **kwargs):
		objEx= OrderProduct.objects.filter(id=self.kwargs['pk'])
		if objEx.count()<=0:
			return HttpResponse('<h4><code> This object not exist in the list. </code></h4>')
		self.object = self.get_object()
		return super(DeleteCart, self).get(request, *args, **kwargs)


class DeleteCartSearch(SuccessMessageMixin, DeleteView):
	model = OrderProduct 
	success_message = " Deleted successfully!"
	success_url = reverse_lazy('product:list_cart')
	template_name = 'product/delete_cart_search.html'

	@method_decorator(login_required(''))
	def dispatch(self, request, *args, **kwargs):	
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	@method_decorator(login_required(''))
	def get(self, request, *args, **kwargs):
		objEx= OrderProduct.objects.filter(id=self.kwargs['pk'])
		if objEx.count()<=0:
			return HttpResponse('<h4><code> This object not exist in the list. </code></h4>')
		self.object = self.get_object()
		return super(DeleteCartSearch, self).get(request, *args, **kwargs)


def avtivation_cart(request):
	
	if request.is_ajax():
		myid = request.GET['id']
		myactivation = request.GET['activation']

		if int(myactivation) == 1:
			OrderProduct.objects.filter(id=myid).update(activation=True)
		else:

			OrderProduct.objects.filter(id=myid).update(activation=False)

		return HttpResponse(json.dumps({'data':'success'}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'data':'false'}), content_type="application/json")






