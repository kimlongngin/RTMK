from django.db import models

from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
import os
from django.core.exceptions import ValidationError
from location.models import Location
from product.models import Product

class Customer(models.Model):
	full_name = models.CharField(max_length=255, primary_key=True)
	phone_number = models.CharField(max_length=50, blank=True)
	email = models.CharField(max_length=255, blank=True)
	province = models.ForeignKey(Location, on_delete=models.CASCADE)
	address = models.TextField()
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def __str__ (self):
	 	return self.full_name 

	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	        return self.full_name

class SellInvoice(models.Model): 
	invoice_number = models.CharField(max_length=255, primary_key=True) # will auto generated
	user = models.ForeignKey(User, related_name='sell_invoice_users', on_delete=models.CASCADE) # who are sell this product
	customer = models.OneToOneField(Customer, related_name='sell_invoice_customer', on_delete=models.CASCADE)
	description= models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)
	
	def __str__ (self):
	 	return self.user 

	class Meta:
		ordering = ["-created_at", "-updated_at"]

class SellInvoiceItem(models.Model):
	invoice = models.ForeignKey(SellInvoice, related_name='sell_invoice_item', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='invoice_item_product', on_delete=models.CASCADE)
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
