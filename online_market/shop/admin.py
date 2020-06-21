from django.contrib import admin
from . import models

@admin.register(models.ItemModel)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['__str__']


@admin.register(models.UserModel)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['__str__']
