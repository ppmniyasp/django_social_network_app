# Generated by Django 4.2.6 on 2023-10-22 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_chat_participants'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfileModel',
        ),
    ]