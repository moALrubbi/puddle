from django.db import migrations, models
from django.contrib.auth.models import User

def set_default_user(apps, schema_editor):
    CartItem = apps.get_model('cart', 'CartItem')

    # Set a default user for existing rows with null value
    default_user = User.objects.get(id=3)  # Set your default user ID here

    CartItem.objects.filter(user=None).update(user=default_user)

class Migration(migrations.Migration):
    dependencies = [
        ('cart', '0005_remove_cartitem_cart_cartitem_user'),  # Update this line
    ]
    # Rest of your migration file...

    # rest of your migration file...

    operations = [
        migrations.RunPython(set_default_user),
        migrations.AlterField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, to='auth.User')
        ),
    ]
