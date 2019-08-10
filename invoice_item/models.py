from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
import os
from django.core.exceptions import ValidationError
from client.models import Client
from invoice.models import Invoice
from product.models import Product

class InvoiceItem(models.Model):
	invoice = models.OneToOneField(Invoice, related_name='invoice_item', on_delete=models.CASCADE)
	# product = models.OneToOneField(Product, related_name='invoice_item_product', on_delete=models.CASCADE)
	unit= models.IntegerField(default=0)
	unit_price = models.FloatField(default=0.0)
	description= models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)
	
	# def get_absolute_url(self):
	# 	return reverse('linkedhr:detail', kwargs={'pk':self.pk})
	
	def __str__ (self):
		return self.invoice
	class Meta:
		ordering = ["-created_at", "-updated_at"]
