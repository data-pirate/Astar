# Generated by Django 3.0.3 on 2020-03-03 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_delete_item_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='shop/product_images'),
        ),
    ]