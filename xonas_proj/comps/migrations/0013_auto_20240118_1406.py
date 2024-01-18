# Generated by Django 3.2.16 on 2024-01-18 14:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comps', '0012_auto_20240110_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='gender',
            field=models.CharField(default='m', max_length=32, verbose_name='Пол'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='turnover_days',
            field=models.PositiveIntegerField(default=0, verbose_name='Оборачиваемость'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favorites',
            name='sku_first_date',
            field=models.DateTimeField(default=datetime.date(2024, 1, 18), verbose_name='Дата появления'),
        ),
    ]