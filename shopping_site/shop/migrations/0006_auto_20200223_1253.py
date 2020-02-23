# Generated by Django 3.0.2 on 2020-02-23 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200223_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='this eas a test', max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('Hot', 'hot'), ('New', 'new'), ('Sale', 'sale')], max_length=4, null=True),
        ),
    ]