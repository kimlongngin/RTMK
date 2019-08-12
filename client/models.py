from django.db import models
from location.models import Location

class Client(models.Model):
	name = models.CharField(max_length=255, primary_key=True)
	phone_number = models.CharField(max_length=50)
	email = models.CharField(max_length=255)
	province = models.ForeignKey(Location, on_delete=models.CASCADE)
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
