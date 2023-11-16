from django.apps import AppConfig
from django.db import IntegrityError, OperationalError, ProgrammingError


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product"

    def ready(self):
        # Import your model inside the method to avoid circular imports.
        from .models import Category
        try:
            Category.objects.get_or_create(
                name="All", defaults={"description": "All categories"})
        # To handle cases like initial migration where DB table might not exist yet.
        except (IntegrityError, OperationalError, ProgrammingError):
          pass
