from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.users_list, name='users_list'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
]
