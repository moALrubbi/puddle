# Generated by Django 4.2.6 on 2023-11-14 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0008_remove_cart_items_cart_total_price_alter_cart_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkout', '0004_alter_order_items_alter_order_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='checkout.OrderItem', to='item.item'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item'),
        ),
    ]
