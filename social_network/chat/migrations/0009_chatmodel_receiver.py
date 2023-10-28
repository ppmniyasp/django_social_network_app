# Generated by Django 4.2.6 on 2023-10-24 02:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0008_rename_is_read_chatmodel_is_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messeges', to=settings.AUTH_USER_MODEL),
        ),
    ]