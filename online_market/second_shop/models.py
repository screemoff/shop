from django.db import models

class UserItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=20000)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    price = models.IntegerField()
    user = models.ForeignKey('shop.UserModel', related_name='my_items', on_delete=models.CASCADE)
    category = models.CharField(
        choices=[('iphone', 'IPhone'), ('ipad', 'IPad'), ('mac', 'MacBook'), ('airpods', 'AirPods')], max_length=200)


    def __str__(self):
        return self.title
