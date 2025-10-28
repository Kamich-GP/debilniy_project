from django.shortcuts import render
from .models import *

# Create your views here.
def home_page(request):
    all_categories = Category.objects.all()
    all_products = Product.objects.all()
    context = {
        "categories": all_categories,
        "products": all_products
    }
    return render(request, 'home.html', context)
