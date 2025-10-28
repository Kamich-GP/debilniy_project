from django.db import models

# Create your models here.
# Таблица категорий
class Category(models.Model):
    category_name = models.CharField(max_length=32, verbose_name='Название категории')
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

# Таблица продуктов
class Product(models.Model):
    product_name = models.CharField(max_length=128, verbose_name='Название')
    product_des = models.TextField(verbose_name='Описание')
    product_count = models.IntegerField(verbose_name='Кол-во товара')
    product_price = models.IntegerField(verbose_name='Цена товара')
    product_photo = models.ImageField(upload_to='media', verbose_name='Фото')
    product_category = models.ForeignKey(Category,
                                         on_delete=models.CASCADE,
                                         verbose_name='Категория')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

# Таблица корзины
class Cart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_pr_amount = models.IntegerField()

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'
