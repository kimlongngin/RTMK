from django.contrib import admin

from django.contrib.auth.models import User
from .models import Customer, SaleInvoice, SaleInvoiceItem, SaleInvoiceItemHistory
from django.contrib.auth.models import Group 
from django.contrib.admin.models import LogEntry, ADDITION
import os
from django.contrib.admin import helpers
from django.template.response import TemplateResponse

from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _, gettext_lazy


class CustomerAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'phone_number', 'email', 'province', 'address', 'created_at', 'is_status')
	search_fields = ('full_name', 'phone_number', 'email', 'province', 'address')

admin.site.register(Customer, CustomerAdmin)


class SaleInvoiceAdmin(admin.ModelAdmin):
	list_display = ('invoice_number', 'user', 'customer', 'updated_at')
	search_fields = ('invoice_number', 'user', 'customer', 'updated_at')
admin.site.register(SaleInvoice, SaleInvoiceAdmin)


class SaleInvoiceItemAdmin(admin.ModelAdmin):
	list_display = ('invoice', 'product', 'unit', 'unit_price', 'created_at')
	search_fields = ('invoice', 'product')
	# view_on_site = False
	# actions = ['delete_selected']
	# list_per_page = 10 


	# def save_model(self, request, obj, form, change):
	# 	obj.user = request.user
	# 	objID = obj.id
	# 	SaleObj = SaleInvoiceItem.objects.filter(id=objID, is_status="True").count()
		
	# 	if SaleObj:
	# 		super().save_model(request, obj, form, change)

	# 		# Copy product to product's history table "ProductInStockHistory" => Action "UPD"
	# 		# 1 if check this product has in the table then, this script is for update buttion, 
	# 		# 2 otherwise is for save button
	# 		SaleItemHistory = SaleInvoiceItemHistory.objects.create(
	# 			invoice = obj.invoice,
	# 			product = obj.product,
	# 			unit = obj.unit,
	# 			unit_price = obj.unit_price,
	# 			description = obj.description,
	# 			created_at = obj.created_at,
	# 			action = 'UPD'
	# 		)
	# 		SaleItemHistory.save()

	# 	else:
	# 		# Copy product to product's history table "ProductInStockHistory" => Action "SVE"
	# 		# 1 if check this product has in the table then, this script is for update buttion, 
	# 		# 2 otherwise is for save button
	# 		super().save_model(request, obj, form, change)
	# 		SaleItemHistory = SaleInvoiceItemHistory.objects.create(
	# 			invoice = obj.invoice,
	# 			product = obj.product,
	# 			unit = obj.unit,
	# 			unit_price = obj.unit_price,
	# 			description = obj.description,
	# 			created_at = obj.created_at,
	# 			action = 'SVE'
	# 		)
	# 		SaleItemHistory.save()

	# def delete_model(self, request, obj):
	# 	if request.POST:
	# 		obj.user = request.user
	# 		super().delete_model(request, obj)
	# 		SaleItemHistory = SaleInvoiceItemHistory.objects.create(
	# 			invoice = obj.invoice,
	# 			product = obj.product,
	# 			unit = obj.unit,
	# 			unit_price = obj.unit_price,
	# 			description = obj.description,
	# 			created_at = obj.created_at,
	# 			action = 'DEL'
	# 		)
	# 		SaleItemHistory.save()
		
admin.site.register(SaleInvoiceItem, SaleInvoiceItemAdmin)



class SaleInvoiceItemHistoryAdmin(admin.ModelAdmin):
	list_display = ('invoice', 'product', 'unit', 'unit_price', 'created_at')
	search_fields = ('invoice', 'product')
	

admin.site.register(SaleInvoiceItemHistory, SaleInvoiceItemHistoryAdmin)

# Register your models here.
