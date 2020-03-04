from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')

admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Profile, ProfileAdmin)