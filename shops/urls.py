from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.shops_page, name='shops_page'),
    path('shop/<int:id>', views.shop_details_page, name='shop_details_page'),
]
