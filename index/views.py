from django.shortcuts import render
from .models import *

# Create your views here.
# Главная страница
def home_page(request):
    # Достаем данные из БД
    all_categories = Category.objects.all()
    all_products = Product.objects.all()
    # Передаем данные на Frontend
    context = {
        "categories": all_categories,
        "products": all_products
    }
    return render(request, 'home.html', context)

# Страница с выбранной категорией
def category_page(request, pk):
    # Достаем данные из БД
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category=category)
    # Передаем данные на Frontend
    context = {
        "category": category,
        "products": products
    }
    return render(request, 'category.html', context)

# Страница с выбранным товаром
def product_page(request, pk):
    # Достаем данные из БД
    product = Product.objects.get(id=pk)
    # Передаем данные на Frontend
    context = {"product": product}
    return render(request, 'product.html', context)
