from django.contrib import admin
from django.contrib.auth.models import User
from .models import Media, OrderProduct, Product,ProductType, ProductHistory, ProductUnit, ProductCategory, ProductInStock, SubProductImage, Promotion, ProductInStockHistory, StockLocation
from django.contrib.auth.models import Group 
from django.contrib.admin.models import LogEntry, ADDITION
import os
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from .decorators import action_form


from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import model_ngettext
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _, gettext_lazy




admin.site.register(ProductCategory)

admin.site.register(Product)

admin.site.register(SubProductImage)

admin.site.register(Promotion)

admin.site.register(StockLocation)
		
admin.site.register(ProductType)

admin.site.register(OrderProduct)

admin.site.register(Media)
		







