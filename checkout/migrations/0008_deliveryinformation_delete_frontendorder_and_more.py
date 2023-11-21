# Generated by Django 4.2.6 on 2023-11-21 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkout', '0007_frontendorder_delete_checkoutinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('street_name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('building_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('additional_delivery_info', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='FrontendOrder',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
    ]