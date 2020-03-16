from django.contrib import admin
from .models import *

class ItemAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'price')
    list_filter = ('price', 'title')
    search_fields = ('user__username', 'title')
    list_editable = ('price',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImages)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Profile, ProfileAdmin)