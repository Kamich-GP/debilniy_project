from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views import View
import telebot

# Создаем объект бота
bot = telebot.TeleBot('TOKEN')
admin_id = 'ADMIN_ID'

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

# Регистрация (класс представления)
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {'form': RegForm}
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            User.objects.create_user(username=username,
                                     email=email,
                                     password=password).save()
            return redirect('/reg-end')

# Окончание регистрации
def reg_end(request):
    return render(request, 'registration/reg_end.html')

# Выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect('/')

# Поиск товара по названию
def search(request):
    if request.method == 'POST':
        # Достаем данные с формы
        get_product = request.POST.get('search_product')
        # Достаем данные из БД
        searched_product = Product.objects.filter(product_name__iregex=get_product)
        context = {}
        if searched_product:
            context.update(products=searched_product, request=get_product)
        else:
            context.update(products='', request=get_product)
        return render(request, 'result.html', context)

# Добавление товара в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        user_count = int(request.POST.get('pr_amount'))
        print(user_count)

        if 1 <= user_count <= product.product_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_amount=user_count).save()
            return redirect('/')
        return redirect(f'/product/{pk}')

# Удаление товара из корзины
def del_from_cart(request, pk):
    Cart.objects.filter(user_product=Product.objects.get(id=pk)).delete()
    return redirect('/cart')

# Отображение корзины
def show_cart(request):
    # Достаем данные из БД
    user_cart = Cart.objects.filter(user_id=request.user.id)
    # Итоговые суммы за каждые позиции в корзине
    totals = [round(t.user_product.product_price * t.user_pr_amount, 2)
              for t in user_cart]
    context = {
        'cart': user_cart,
        'total': round(sum(totals, 2))
    }

    if request.method == 'POST':
        text = (f'Новый заказ!\n'
                f'Клиент: {User.objects.get(id=request.user.id).email}\n\n')

        for i in user_cart:
            product = Product.objects.get(id=i.user_product.id)
            product.product_count = product.product_count - i.user_pr_amount
            product.save(update_fields=['product_count'])
            text += f'Товар: {i.user_product}\nКоличество: {i.user_pr_amount}\n\n'

        text += f'Итого: ${round(sum(totals), 2)}'
        bot.send_message(admin_id, text)
        user_cart.delete()
        return redirect('/')

    return render(request, 'cart.html', context)
