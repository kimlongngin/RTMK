from django.db import models


# Create your models here.

class Client(models.Model):
	name = models.CharField(max_length=255, primary_key=True)
	phone_number = models.CharField(max_length=50)
	email = models.CharField(max_length=255)
	address = models.TextField()
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
