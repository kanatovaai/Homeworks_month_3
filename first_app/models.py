from django.db import models


# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Каегории'

    name = models.CharField(max_length=200, verbose_name='Название', blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(max_length=200, verbose_name='Название', blank=False)
    description = models.CharField('Описание', max_length=500, blank=False)
    price = models.IntegerField('Цена', default=None, blank=False)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    text = models.CharField('Текст', max_length=500, blank=False)
    # author = models.CharField('Пользователь', max_length=200, blank=False)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text
