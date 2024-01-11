from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import stripe
from django.db.models.signals import post_save
from django.dispatch import receiver
from stripe_app.models import Item, Order, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY


def get_stripe_session_id(request, id):
    item = get_object_or_404(Item, id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),  # convert to cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return JsonResponse({'session_id': session.id})


def get_item_page(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item.html',
                  {'name': item.name, 'description': item.description, 'price': item.price, 'currency': item.currency})


@receiver(post_save, sender=Order)
def process_payment(sender, instance, created, **kwargs):
    if created:
        items = instance.items.all()
        total_cost = sum(item.price for item in items)

        payment = stripe.PaymentIntent.create(
            amount=total_cost,
            currency='usd',
        )

        if instance.discount:
            stripe.Discount.create(amount=instance.discount.amount, order=instance.discount.order)
        if instance.tax:
            stripe.Tax.create(rate=instance.tax.rate, order=instance.tax.order)

        Payment.objects.create(order=instance, payment_id=payment.id)

        instance.total_cost = total_cost
        instance.save()
