from django.contrib import admin

from .models import Product, ProductHistory, ProductUnit, ProductCategory, ProductInStock, SubProductImage, Promotion, ProductInStockHistory
from django.contrib.auth.models import Group 

	
admin.site.register(ProductCategory)

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'product_number', 'serial_number', 'created_at')
	search_fields = ('name', 'product_number', 'serial_number')
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductUnit)

class ProductHistoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'product_number', 'serial_number', 'created_at')
	search_fields = ('name', 'product_number', 'serial_number')

admin.site.register(ProductHistory, admin.ModelAdmin)

class ProductInStockAdmin(admin.ModelAdmin):
	list_display = ('product', 'title', 'unit_title', 'unit', 'created_at')
	search_fields = ('product', 'title')
admin.site.register(ProductInStock)


admin.site.register(SubProductImage)
admin.site.register(Promotion)
admin.site.register(ProductInStockHistory)

# admin.site.unregister(Group)






