# Generated by Django 4.2.6 on 2023-12-14 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0012_remove_item_favorited_by_item_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='favorites',
            new_name='favorited_by',
        ),
    ]
