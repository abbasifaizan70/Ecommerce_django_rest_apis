# Generated by Django 4.2.5 on 2023-10-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0007_remove_product_images_alter_productimage_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
