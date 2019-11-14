# in project/app/context_processors.py
from app.models import Product, Media

def base_media(request):
    return {'all_media': Media.objects.all()} # of course some filter here