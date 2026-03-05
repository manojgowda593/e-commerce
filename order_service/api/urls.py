from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.orders_list, name='orders_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
