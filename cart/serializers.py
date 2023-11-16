from rest_framework import serializers
from .models import Cart, CartItem, TransactionHistory, ShippingInformation
from product.models import Product, ProductImage
from django.core.validators import MinValueValidator


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('image_url',)
        ref_name = 'CartProductImageSerializer'

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'category', 'images', 'stock')
        ref_name = 'CartProductSerializer'


class CartItemSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(source='get_total_price', read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)
    quantity = serializers.IntegerField(
        validators=[MinValueValidator(-1)]
    )

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_detail',
                  'quantity', 'total', 'added_at')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.FloatField(
        source='get_total_cart_price', read_only=True)
    count = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at',
                  'updated_at', 'total', 'count')

    # Add this method to get the count
    def get_count(self, obj):
        return obj.items.count()


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'

class ShippingInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInformation
        fields = '__all__'