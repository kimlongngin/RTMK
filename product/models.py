from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# from tinymce.models import HTMLField

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
    	# return self.name + ' ' + str(self.created_at)
    	return self.name 

    class  Meta:
    	ordering = ['created_at']

def upload_location(instance, filename):
		filebase, extension = filename.split(".")
		return "%s/%s.%s" %(instance.id, instance.id, extension)

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def user_directory_path(request, filename):
	# return "files/users/%s/%s" % (request.user.id, filename)
    return '/'.join(['content', request.name, filename])

def increment_product_number():
	last_product = Product.objects.all().order_by('id').last()
	if not last_product:
		return 'RTMK00001'
	width = 5
	product_number = last_product.product_number
	product_int = int(product_number.split('RTMK')[-1])
	new_product_int = product_int + 1
	formatted = (width - len(str(new_product_int))) * "0" + str(new_product_int)
	new_product_int = 'RTMK' + str(formatted)
	return str(new_product_int)

class Product(models.Model):
	product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	product_number = models.CharField(max_length=500, null=True, blank=True, 
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$',
        message='Produce number must be Alphanumeric',code='Number is invalide'),], 
        default=increment_product_number)
	serial_number = models.CharField(max_length=150, default=0, null=True, blank=True)
	default_image = models.FileField(blank=True, upload_to=user_directory_path,  validators=[validate_file_extension])
	size = models.CharField(max_length=250, default="", null=True, blank=True)
	color = models.CharField(max_length=20, default="", null=True, blank=True)
	price =  models.FloatField(default=0.0) # Price for each product item in per/unit
	special_price = models.FloatField(default=0.0) # In case some clients buy many products
	description = models.TextField()
	review = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def get_absolute_url(self):
			return reverse('product:detail', kwargs={'pk':self.pk})

	def __str__ (self):
		return self.name

	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	        return self.name

class Rate(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rate_number = models.FloatField(default=0.0)
	rate = models.FloatField(default=0.0)
	is_status = models.BooleanField(default=True)
	

class SubProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	name = models.CharField(max_length = 150)
	sub_image = models.FileField(blank=True, upload_to=user_directory_path,  validators=[validate_file_extension])
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def __str__ (self):
		return self.name

	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	    	return self.name

class ProductInStock(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	title = models.CharField(max_length=150, null=True, blank=True)
	unit_title = models.CharField(max_length=250) # Bottle, Tube, Box 
	unit = models.IntegerField(default=0) # Amount of Unit
	amount_per_unit =  models.IntegerField(default=0) # Amount product of product in stock per Unit
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def __str__ (self):
		return self.title

	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	        return self.title

class Promotion(models.Model):
	title = models.CharField(max_length=200, null=True, blank=None)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	discount_as_percentag = models.IntegerField(default=0) 
	discount_as_price = models.FloatField(default=0.0) 
	description = models.TextField()
	start_date_discount = models.DateTimeField(auto_now=False, auto_now_add=False)
	end_date_discount = models.DateTimeField(auto_now=False, auto_now_add=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def __str__ (self):
		return self.title
	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	        return self.title

class ProductUnit(models.Model):
	title = models.CharField(max_length=255)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	unit = models.CharField(max_length=255)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def __str__ (self):
		return self.title

	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	        return self.title


class ProductInStockHistory(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	title = models.CharField(max_length=150, null=True, blank=True)
	unit_title = models.CharField(max_length=250) # Bottle, Tube, Box 
	unit = models.IntegerField(default=0) # Amount of Unit
	amount_per_unit =  models.IntegerField(default=0) # Amount product of product in stock per Unit
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def __str__ (self):
		return self.title

	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	        return self.title

# All products will store in producthistory table
# Including adding new products, update product 
class ProductHistory(models.Model):
	product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	product_number = models.CharField(max_length=500, null=True, blank=True, 
        validators=[RegexValidator(regex='^[a-zA-Z0-9]*$',
        message='Produce number must be Alphanumeric',code='Number is invalide'),], 
        default=increment_product_number)
	serial_number = models.CharField(max_length=150, default=0, null=True, blank=True)
	default_image = models.FileField(blank=True, upload_to=user_directory_path,  validators=[validate_file_extension])
	size = models.CharField(max_length=250, null=True, blank=True)
	color = models.CharField(max_length=20, null=True, blank=True)
	rice =  models.FloatField(default=0.0) # Price for each product item in per/unit
	special_pprice = models.FloatField(default=0.0) # In case some clients buy many products
	description = models.TextField()
	review = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)

	def get_absolute_url(self):
			return reverse('product:detail', kwargs={'pk':self.pk})

	def __str__ (self):
		return self.name

	class Meta:
	    ordering = ['created_at']
	    def __unicode__(self):
	        return self.name




