from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    min_num = 1


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["images"]

    def clean(self):
        cleaned_data = super().clean()

        # For new product creations or updates
        if not self.instance.pk or "images-TOTAL_FORMS" in self.data:
            total_images = int(self.data.get("images-TOTAL_FORMS", 0))

            # Count how many image inlines have actual uploaded files
            actual_images = sum(
                1 for i in range(total_images) if f"images-{i}-image" in self.files
            )

            # Check if an existing product has images and if it's being edited without new images
            if self.instance.pk:
                existing_images_count = self.instance.images.count()
                actual_images += existing_images_count

            if actual_images < 1:
                raise ValidationError("At least one image must be attached.")

        return cleaned_data


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm  # Use the custom form
    list_display = ("name", "category", "price", "stock", "created_at", "updated_at")
    list_filter = ("category",)
    search_fields = ("name", "description")
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "created_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
