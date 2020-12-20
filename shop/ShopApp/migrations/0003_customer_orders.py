# Generated by Django 3.1.3 on 2020-12-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(related_name='related_order', to='ShopApp.Order', verbose_name='Заказы покупателя'),
        ),
    ]
