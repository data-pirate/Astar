# Generated by Django 3.0.3 on 2020-03-07 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20200307_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='discount price (optional)'),
        ),
    ]
