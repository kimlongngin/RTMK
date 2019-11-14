from django.apps import AppConfig
from product.models import Product, Media

class ProductConfig(AppConfig):
    name = 'product'

def base_media(request):
    return {'all_media': Media.objects.all()} # of course some filter here