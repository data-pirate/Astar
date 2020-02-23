from django.db import models
from django.conf import settings
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('men', 'Men'),
    ('women', 'Women')
)

SUB_CATEGORY = (
    ('Shirts', 'Shirts'),
    ('Dress', 'Dresses'),
    ('Jeans', 'Jeans'),
    ('Shoes', 'Shoes'),
    ('purse', 'Purse')
)
LABELS = (
    ('Hot', 'hot'),
    ('New', 'new'),
    ('Sale', 'sale')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    sub_category = models.CharField(choices=SUB_CATEGORY, max_length=6)
    label = models.CharField(choices=LABELS, null=True,
                             blank=True, max_length=4)
    description = models.CharField(max_length=2000)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'pk': self.id,
            'slug': self.slug
        })

    def get_cart_url(self):
        return reverse("shop:add_to_cart", kwargs={
            'pk': self.id,
            'slug': self.slug
        })
    
    def remove_from_cart_url(self):
        return reverse("shop:remove_from_cart", kwargs={
            'pk': self.id,
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username
