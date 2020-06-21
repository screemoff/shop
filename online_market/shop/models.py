from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse

class UserModel(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    money = models.IntegerField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    EMAIL_FIELD = 'email'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})

    def __str__(self):
        return self.username

class ItemModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=20000)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    price = models.IntegerField()
    users = models.ManyToManyField(UserModel, related_name='trash', blank=True)
    category = models.CharField(choices=[('iphone', 'IPhone'), ('ipad', 'IPad'), ('mac', 'MacBook'), ('airpods', 'AirPods')], max_length=500)

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class ChatModel(models.Model):
    user_from = models.ForeignKey(UserModel, related_name='chats_from_me', related_query_name='chat_from_me', on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserModel, related_name='chats_to_me', related_query_name='chat_to_me', on_delete=models.CASCADE)
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE, default=None)


class MessageModel(models.Model):
    chat = models.ForeignKey(ChatModel, related_name='messages', related_query_name='message', on_delete=models.CASCADE)
    text = models.CharField(max_length=5000)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)