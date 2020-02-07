# Generated by Django 3.0.2 on 2020-02-07 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('category', models.CharField(default='', max_length=100)),
                ('sub_category', models.CharField(default='', max_length=100)),
                ('price', models.FloatField(default=0)),
                ('desc', models.CharField(default='', max_length=200)),
                ('date', models.DateField()),
                ('image', models.ImageField(default='', upload_to='shop/product_images')),
            ],
        ),
    ]