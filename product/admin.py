from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product, ProductHistory, ProductUnit, ProductCategory, ProductInStock, SubProductImage, Promotion, ProductInStockHistory
from django.contrib.auth.models import Group 
from django.contrib.admin.models import LogEntry, ADDITION
import os

class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'is_status')
	search_fields = ['name']

admin.site.register(ProductCategory, ProductCategoryAdmin)
	

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'product_number', 'serial_number', 'created_at', 'is_status')
	search_fields = ('name', 'product_number', 'serial_number')

	# def save_model(self, request, obj, form, change):
	# 	#obj.save()

	# 	category = obj.product_category
	# 	print(category)
	# 	return category
		# name = obj.name
		# product_number = obj.product_number
		# serial_number = obj.serial_number
		# default_image = obj.default_image
		# size =obj.size
		# color = obj.color
		# price = obj.price
		# special_price = obj.special_price
		# description = obj.description
		# review = obj.review
		# action = "save"
		# ProductHistory.save_model(obj)

		# super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)


class ProductUnitAdmin(admin.ModelAdmin):
	list_display = ('title', 'product', 'created_at', 'is_status')
	search_fields = ('product__name', 'title')
admin.site.register(ProductUnit, ProductUnitAdmin)


class ProductHistoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'product_number', 'serial_number', 'created_at')
	search_fields = ('name', 'product_number', 'serial_number')

admin.site.register(ProductHistory, admin.ModelAdmin)
	



def delete_selected(self, request, queryset):
	if request.method == "POST":
		for obj in queryset:
			obj.delete()
			History = ProductInStockHistory.objects.create(
				product = obj.product,
				title = obj.title,
				unit_title = obj.unit_title,
				unit = obj.unit,
				amount_per_unit =  obj.amount_per_unit,
				description = obj.description,
				action = 'DEL'
			)
			History.save()

	# queryset.update(status='p')
delete_selected.short_description = "Delete"
# Delete selected product in stock historys

class ProductInStockAdmin(admin.ModelAdmin):
	

	list_display = ('product', 'title', 'unit_title', 'unit', 'amount_per_unit', 'created_at', 'is_status')
	search_fields = ('product__name', 'title')
	# list_display_links = None
	view_on_site = False
	actions = [delete_selected]

	def delete_model(self, request, obj):
		if request.POST:
			obj.user = request.user
			super().delete_model(request, obj)
			History = ProductInStockHistory.objects.create(
			product = obj.product,
			title = obj.title,
			unit_title = obj.unit_title,
			unit = obj.unit,
			amount_per_unit =  obj.amount_per_unit,
			description = obj.description,
			action = 'DEL'
		)
		History.save()


	def save_model(self, request, obj, form, change):
		obj.user = request.user
		super().save_model(request, obj, form, change)

		# Copy product to product's history table "ProductInStockHistory" => Action "SAVE"
		# 1 if check this product has in the table then, this script is for update buttion, 
		# 2 otherwise is for save button
		History = ProductInStockHistory.objects.create(
			product = obj.product,
			title = obj.title,
			unit_title = obj.unit_title,
			unit = obj.unit,
			amount_per_unit =  obj.amount_per_unit,
			description = obj.description,
			action = 'SAVE'
		)
		History.save()

admin.site.register(ProductInStock, ProductInStockAdmin)



class SubProductImageAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at', 'is_status')
	search_fields = ('product__name', 'name')
admin.site.register(SubProductImage, SubProductImageAdmin)


class PromotionAdmin(admin.ModelAdmin):
	list_display = ('title', 'product', 'created_at', 'is_status')
	search_fields = ('product__name', 'title')

admin.site.register(Promotion, PromotionAdmin)



class ProductInStockHistoryAdmin(admin.ModelAdmin):

	list_display = ('product', 'title', 'unit_title', 'unit', 'amount_per_unit', 'created_at', 'is_status')
	search_fields = ('product__name', 'title')

	def delete_model(self, request, obj):
		if request.POST:
			obj.user = request.user
			super().delete_model(request, obj)
		
admin.site.register(ProductInStockHistory, ProductInStockHistoryAdmin)

# admin.site.unregister(Group)






