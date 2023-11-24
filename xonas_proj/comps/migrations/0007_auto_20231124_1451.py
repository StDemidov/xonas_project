# Generated by Django 3.2.16 on 2023-11-24 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comps', '0006_alter_sku_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku',
            name='price_graph',
        ),
        migrations.RemoveField(
            model_name='sku',
            name='sells_graph',
        ),
        migrations.RemoveField(
            model_name='sku',
            name='stocks_graph',
        ),
        migrations.RemoveField(
            model_name='sku',
            name='thumb',
        ),
        migrations.AddField(
            model_name='sku',
            name='avg_sells14',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж 14 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='avg_sells21',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж 21 день'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='avg_sells30',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж 30 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='avg_sells8',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='boost14',
            field=models.BooleanField(default=1, verbose_name='Флаг буста 14 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='boost21',
            field=models.BooleanField(default=1, verbose_name='Флаг буста 21 день'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='boost30',
            field=models.BooleanField(default=1, verbose_name='Флаг буста 30 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='boost8',
            field=models.BooleanField(default=1, verbose_name='Флаг буста 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='median_price14',
            field=models.FloatField(default=1, verbose_name='Медианная цена 14 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='median_price21',
            field=models.FloatField(default=1, verbose_name='Медианная цена 21 день'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='median_price30',
            field=models.FloatField(default=1, verbose_name='Медианная цена 30 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='median_price8',
            field=models.FloatField(default=1, verbose_name='Медианная цена 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_graph14',
            field=models.TextField(default=1, verbose_name='Продажи 14 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_graph21',
            field=models.TextField(default=1, verbose_name='Продажи 21 день'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_graph30',
            field=models.TextField(default=1, verbose_name='Продажи 30 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_graph8',
            field=models.TextField(default=1, verbose_name='Продажи 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_stocks14',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж/стоков 14 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_stocks21',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж/стоков 21 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_stocks30',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж/стоков 30 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='sells_stocks8',
            field=models.BooleanField(default=1, verbose_name='Флаг продаж/стоков 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks14',
            field=models.BooleanField(default=1, verbose_name='Флаг остатков 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks21',
            field=models.BooleanField(default=1, verbose_name='Флаг остатков 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks30',
            field=models.BooleanField(default=1, verbose_name='Флаг остатков 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks8',
            field=models.BooleanField(default=1, verbose_name='Флаг остатков 8 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks_graph14',
            field=models.TextField(default=1, verbose_name='Остатки 14 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks_graph21',
            field=models.TextField(default=1, verbose_name='Остатки 21 день'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks_graph30',
            field=models.TextField(default=1, verbose_name='Остатки 30 дней'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sku',
            name='stocks_graph8',
            field=models.TextField(default=1, verbose_name='Остатки 8 дней'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sku',
            name='thumb_middle',
            field=models.CharField(max_length=256, verbose_name='Картинка 1'),
        ),
        migrations.CreateModel(
            name='Sku_stats8',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skus', to='comps.sku', verbose_name='Товар')),
            ],
        ),
    ]