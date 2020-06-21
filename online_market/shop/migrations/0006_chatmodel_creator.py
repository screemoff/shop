# Generated by Django 3.0.5 on 2020-06-07 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_chatmodel_messagemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
