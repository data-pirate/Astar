# Generated by Django 3.0.2 on 2020-02-23 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_orderitem_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='category',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='label',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('men', 'Men'), ('women', 'Women')], default='test', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('Hot', 'Hot'), ('New', 'New'), ('Sale', 'Sale')], default='test', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='sub_category',
            field=models.CharField(choices=[('Shirts', 'Shirts'), ('Dress', 'Dresses'), ('Jeans', 'Jeans'), ('Shoes', 'Shoes'), ('purse', 'Purse')], default='test', max_length=6),
            preserve_default=False,
        ),
    ]