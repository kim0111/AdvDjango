from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView

# from .views import ProductViewSet


urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category_list_create"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("products/", ProductListCreateView.as_view(), name="product_list_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
