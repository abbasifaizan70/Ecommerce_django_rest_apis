from django.contrib import admin

from .models import Cart, CartItem, TransactionHistory


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "total_price", "transaction_date", "stripe_charge_id")

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at", "stripe_charge_id", "cart_total_price")

    def cart_total_price(self, obj):
        return obj.total_price
    cart_total_price.short_description = 'Total Price'

admin.site.register(CartItem)
