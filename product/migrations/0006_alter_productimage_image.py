# Generated by Django 4.2.5 on 2023-10-11 12:30

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0005_productimage_product_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, verbose_name="image"
            ),
        ),
    ]
