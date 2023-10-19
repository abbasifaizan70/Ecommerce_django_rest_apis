from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<slug:category_slug>/",
        views.CategoryRetrieveView.as_view(),
        name="category-detail",
    ),
    path('search/', views.ProductSearchView.as_view(), name='product-search'),
    path("", views.ProductListView.as_view(), name="product-list"),
    path(
        "<int:product_id>",
        views.ProductRetrieveView.as_view(),
        name="product-detail",
    ),
]
