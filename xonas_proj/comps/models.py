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
    img = models.CharField(
        max_length=256,
        verbose_name='Картинка',
        default='#'
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
    thumb_middle = models.CharField(max_length=256, verbose_name='Картинка 1')
    sku_first_date = models.DateTimeField(verbose_name='Дата появления')
    median_price8 = models.FloatField(verbose_name='Медианная цена 8 дней')
    sells_graph8 = models.TextField(verbose_name='Продажи 8 дней')
    stocks_graph8 = models.TextField(verbose_name='Остатки 8 дней')
    median_price14 = models.FloatField(verbose_name='Медианная цена 14 дней')
    sells_graph14 = models.TextField(verbose_name='Продажи 14 дней')
    stocks_graph14 = models.TextField(verbose_name='Остатки 14 дней')
    median_price21 = models.FloatField(verbose_name='Медианная цена 21 день')
    sells_graph21 = models.TextField(verbose_name='Продажи 21 день')
    stocks_graph21 = models.TextField(verbose_name='Остатки 21 день')
    median_price30 = models.FloatField(verbose_name='Медианная цена 30 дней')
    sells_graph30 = models.TextField(verbose_name='Продажи 30 дней')
    stocks_graph30 = models.TextField(verbose_name='Остатки 30 дней')
    boost8 = models.BooleanField(verbose_name='Флаг буста 8 дней')
    boost14 = models.BooleanField(verbose_name='Флаг буста 14 дней')
    boost21 = models.BooleanField(verbose_name='Флаг буста 21 день')
    boost30 = models.BooleanField(verbose_name='Флаг буста 30 дней')
    avg_sells8 = models.BooleanField(verbose_name='Флаг продаж 8 дней')
    avg_sells14 = models.BooleanField(verbose_name='Флаг продаж 14 дней')
    avg_sells21 = models.BooleanField(verbose_name='Флаг продаж 21 день')
    avg_sells30 = models.BooleanField(verbose_name='Флаг продаж 30 дней')
    stocks8 = models.BooleanField(verbose_name='Флаг остатков 8 дней')
    stocks14 = models.BooleanField(verbose_name='Флаг остатков 8 дней')
    stocks21 = models.BooleanField(verbose_name='Флаг остатков 8 дней')
    stocks30 = models.BooleanField(verbose_name='Флаг остатков 8 дней')
    sells_stocks8 = models.BooleanField(
        verbose_name='Флаг продаж/стоков 8 дней'
    )
    sells_stocks14 = models.BooleanField(
        verbose_name='Флаг продаж/стоков 14 дней'
    )
    sells_stocks21 = models.BooleanField(
        verbose_name='Флаг продаж/стоков 21 дней'
    )
    sells_stocks30 = models.BooleanField(
        verbose_name='Флаг продаж/стоков 30 дней'
    )

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

    def __str__(self):
        return f'Товар {self.sku_id}'


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
