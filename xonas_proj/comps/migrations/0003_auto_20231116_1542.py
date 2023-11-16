# Generated by Django 3.2.16 on 2023-11-16 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comps', '0002_auto_20231115_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku',
            name='median_price',
        ),
        migrations.AddField(
            model_name='sku',
            name='price_graph',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_graph',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks_graph',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
