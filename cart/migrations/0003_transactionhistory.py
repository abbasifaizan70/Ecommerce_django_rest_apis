# Generated by Django 4.2.5 on 2023-10-16 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("product", "0008_alter_product_slug"),
        ("cart", "0002_cart_stripe_charge_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransactionHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("transaction_date", models.DateTimeField(auto_now_add=True)),
                (
                    "stripe_charge_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]