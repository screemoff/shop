from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.ShopMainView.as_view(), name='shop_main'),
    path('shop/category/', views.CategoryView.as_view(), name='category'),
    path('shop/profile/', views.ProfileView.as_view(), name='profile'),
    path('shop/profile/add_money/', views.AddMoneyView.as_view(), name='add_money'),
    path('shop/profile/delete/', views.delete, name='delete_profile'),
    path('shop/category/item_detail/<int:pk>/', views.ItemView.as_view(), name='item_detail'),
    path('shop/category/item_detail/add_trash/', views.add_trash, name='add_trash'),
    path('shop/profile/trash/', views.TrashView.as_view(), name='trash'),
    path('shop/profile/trash/buy_item/', views.buy_item, name='buy_item'),
    path('shop/profile/trash/delete_item/', views.delete_item, name='delete_item'),
    path('auth_out/', views.auth_out, name='auth_out'),
    path('shop/profile/chats/chat/', views.OneChatView.as_view(), name='chat_view'),
    path('shop/profile/chats/', views.ChatsView.as_view(), name='my_chats'),
    path('item/write_to/', views.WriteMessageView.as_view(), name='write_to_owner'),
    path('shop/profile/chats/delete', views.delete_chat, name='delete_chat'),
]

