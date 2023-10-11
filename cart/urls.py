from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartView.as_view(), name="cart-detail"),
    path("items/", views.CartItemView.as_view(), name="cart-items-list-create"),
    path(
        "items/<int:pk>/",
        views.CartItemDetailView.as_view(),
        name="cart-item-detail-update-delete",
    ),
]
