from django.urls import path
from . import views

urlpatterns = [
    path('', views.shops_page, name='shops_page'),
    path('shop/<int:id>', views.shop_details_page, name='shop_details_page'),
]
