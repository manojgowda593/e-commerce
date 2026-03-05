from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.products_list, name='products_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
