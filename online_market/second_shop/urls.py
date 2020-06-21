from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.SecondShopView.as_view(), name='second_shop'),
    path('add_item/', views.AddItemView.as_view(), name='add_second_shop'),
    path('item/<int:pk>/', views.ItemView.as_view(), name='second_shop_item'),
    path('item/my_items/', views.MyItemsView.as_view(), name='my_items'),
    path('item/my_items/delete_myitem/', views.delete_item, name='delete_myitem'),
    path('item/my_items/change_myitem/', views.ChangeItemView.as_view(), name='change_myitem'),
    path('item/search/', views.SearchView.as_view(), name='search'),
]