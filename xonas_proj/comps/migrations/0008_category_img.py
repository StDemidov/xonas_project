# Generated by Django 3.2.16 on 2023-11-24 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comps', '0007_auto_20231124_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='img',
            field=models.CharField(default='#', max_length=256, verbose_name='Картинка'),
        ),
    ]
