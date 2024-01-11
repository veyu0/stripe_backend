from django.contrib import admin
from .models import Item, Order, Discount, Tax, Payment

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Discount)
admin.site.register(Tax)
