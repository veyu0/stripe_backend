from django.apps import AppConfig
from django.db.utils import OperationalError


class StripeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stripe_app'

    verbose_name = 'Товары'

    def ready(self):
        from .models import Item

        items_data = [
            {
                'name': 'Bag',
                'description': 'White',
                'price': 300
            },
            {
                'name': 'Gucci Bag',
                'description': 'Super',
                'price': 1000
            },
            {
                'name': 'High heel shoes',
                'description': 'D&G',
                'price': 5000
            },
        ]
        try:
            for item_data in items_data:
                Item.objects.get_or_create(**item_data)
        except OperationalError:
            pass
