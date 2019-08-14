from django.contrib import admin

from .models import Customer, SellInvoice, SellInvoiceItem

admin.site.register(Customer)
admin.site.register(SellInvoice)
admin.site.register(SellInvoiceItem)

# Register your models here.
