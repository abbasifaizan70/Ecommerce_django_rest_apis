# Generated by Django 4.2.5 on 2023-10-11 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0006_alter_productimage_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="images",
        ),
        migrations.AlterField(
            model_name="productimage",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="product.product",
            ),
        ),
    ]
