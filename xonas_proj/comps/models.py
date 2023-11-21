from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг',
        unique=True
    )
    min_price = models.PositiveSmallIntegerField(
        verbose_name='Минимальная цена'
    )
    max_price = models.PositiveSmallIntegerField(
        verbose_name='Максимальная цена'
    )
    min_sells = models.PositiveSmallIntegerField(
        verbose_name='Мин. количество продаж в день'
    )
    id_wb = models.CharField(
        blank=True,
        max_length=10,
        verbose_name='ID для API'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name


class Sku(models.Model):
    sku_id = models.CharField(max_length=32, verbose_name='SKU')
    name = models.CharField(max_length=256, verbose_name='Наименование')
    brand = models.CharField(max_length=64, verbose_name='Бренд')
    thumb = models.CharField(max_length=256, verbose_name='Картинка 1')
    thumb_middle = models.CharField(max_length=256, verbose_name='Картинка 2')
    sku_first_date = models.DateTimeField(verbose_name='Дата появления')
    price_graph = models.TextField()
    sells_graph = models.TextField()
    stocks_graph = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='skus',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='fav_users'
    )
    fav = models.ForeignKey(
        Sku,
        on_delete=models.CASCADE,
        verbose_name='Понравившееся',
        related_name='favs'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
