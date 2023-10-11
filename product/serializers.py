from rest_framework import serializers
from cloudinary.templatetags import cloudinary
from .models import Product, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("image_url", "created_at")

    def get_image_url(self, obj):
        return cloudinary.utils.cloudinary_url(obj.image.public_id, format="jpg")[0]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
