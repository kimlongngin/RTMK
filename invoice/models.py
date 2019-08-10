from django.db import models

from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
import os
from django.core.exceptions import ValidationError
from product.models import Product
from client.models import Client


class Invoice(models.Model):
	invoice_number = models.CharField(max_length=255, primary_key=True)
	user_id = models.OneToOneField(User, related_name='invoice_users', on_delete=models.CASCADE)
	client_id = models.OneToOneField(Client, related_name='invoice_client', on_delete=models.CASCADE)
	description= models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	is_status = models.BooleanField(default=True)
	
	# def get_absolute_url(self):
	# 	return reverse('linkedhr:detail', kwargs={'pk':self.pk})

	class Meta:
		ordering = ["-created_at", "-updated_at"]
