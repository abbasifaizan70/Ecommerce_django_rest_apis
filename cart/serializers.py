from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "created_at", "updated_at", "total_price"]
