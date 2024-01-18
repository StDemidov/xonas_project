from django.contrib.auth import get_user_model
from django.db import models
import datetime as dt


User = get_user_model()
today = dt.datetime.today().date()


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
        verbose_name='Мин. сред. количество продаж'
    )
    fix_avg_sells = models.PositiveSmallIntegerField(
        verbose_name='Фикс. сред. количество продаж'
    )
    min_total_sells = models.PositiveSmallIntegerField(
        verbose_name='Мин. количество продаж'
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
    min_avg_sells8 = models.BooleanField(
        blank=True,
        verbose_name='Критерий минимального среднего 8 дней')
    min_avg_sells14 = models.BooleanField(
        blank=True,
        verbose_name='Критерий минимального среднего 14 дней')
    min_avg_sells21 = models.BooleanField(
        blank=True,
        verbose_name='Критерий минимального среднего 21 день')
    min_avg_sells30 = models.BooleanField(
        blank=True,
        verbose_name='Критерий минимального среднего 30 дней')
    fix_avg_8 = models.BooleanField(
        blank=True,
        verbose_name='Фиксированные средние продажи 8 дней')
    fix_avg_14 = models.BooleanField(
        blank=True,
        verbose_name='Фиксированные средние продажи 14 дней')
    fix_avg_21 = models.BooleanField(
        blank=True,
        verbose_name='Фиксированные средние продажи 21 день')
    fix_avg_30 = models.BooleanField(
        blank=True,
        verbose_name='Фиксированные средние продажи 30 дней')
    avg_sells_growth8 = models.BooleanField(
        blank=True,
        verbose_name='Флаг роста продаж 8 дней')
    avg_sells_growth14 = models.BooleanField(
        blank=True,
        verbose_name='Флаг роста продаж 14 дней')
    avg_sells_growth21 = models.BooleanField(
        blank=True,
        verbose_name='Флаг роста продаж 21 день')
    avg_sells_growth30 = models.BooleanField(
        blank=True,
        verbose_name='Флаг роста продаж 30 дней')
    stocks8 = models.BooleanField(
        blank=True,
        verbose_name='Флаг остатков 8 дней')
    stocks14 = models.BooleanField(
        blank=True,
        verbose_name='Флаг остатков 8 дней')
    stocks21 = models.BooleanField(
        blank=True,
        verbose_name='Флаг остатков 8 дней')
    stocks30 = models.BooleanField(
        blank=True,
        verbose_name='Флаг остатков 8 дней')
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
    revenue = models.PositiveBigIntegerField(
        default=0,
        verbose_name='Выручка'
    )
    turnover_days = models.PositiveIntegerField(
        verbose_name='Оборачиваемость'
    )
    gender = models.CharField(max_length=32, verbose_name='Пол')

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

    sku_id = models.CharField(max_length=32, verbose_name='SKU', blank=True)
    name = models.CharField(max_length=256, verbose_name='Наименование', blank=True)
    brand = models.CharField(max_length=64, verbose_name='Бренд', blank=True)
    thumb_middle = models.CharField(max_length=256, verbose_name='Картинка 1', blank=True)
    sku_first_date = models.DateTimeField(verbose_name='Дата появления', default=today)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='favs',
        verbose_name='Категория',
        blank=True
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ExcBrands(models.Model):
    brand = models.CharField(max_length=64, verbose_name='Бренд')

    class Meta:
        verbose_name = 'Исключенный бренд'
        verbose_name_plural = 'Исключенные бренды'
    

class ExcNaming(models.Model):
    word = models.CharField(max_length=128, verbose_name='Слово исключение')

    class Meta:
        verbose_name = 'Слова-исключения для названия'
        verbose_name_plural = 'Слова-исключения для названия'
