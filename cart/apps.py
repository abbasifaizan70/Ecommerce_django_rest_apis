from django.apps import AppConfig
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"
