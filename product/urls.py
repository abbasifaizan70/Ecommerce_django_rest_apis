from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "<slug:category_slug>/",
        views.CategoryRetrieveView.as_view(),
        name="category-detail",
    ),
    # Product URLs
    path("", views.ProductListView.as_view(), name="product-list"),
    path(
        "<slug:category_slug>/<slug:product_slug>/",
        views.ProductRetrieveView.as_view(),
        name="product-detail",
    ),
]
