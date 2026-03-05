from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^user/?.*$', views.proxy_user_service),
    re_path(r'^product/?.*$', views.proxy_product_service),
    re_path(r'^order/?.*$', views.proxy_order_service),
]
