from django.urls import path
from . import views

urlpatterns = [
    path("item/<int:id>", views.item_detail, name="item_detail"),
    path("buy/<int:id>", views.buy_item, name="buy_item"),
    path('items/', views.item_list, name='item_list')
]
