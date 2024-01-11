from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    class Meta:
        app_label = 'stripe_app'


class Order(models.Model):
    items = models.ManyToManyField(Item)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        app_label = 'stripe_app'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'stripe_app'


class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'stripe_app'


class Tax(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        app_label = 'stripe_app'
