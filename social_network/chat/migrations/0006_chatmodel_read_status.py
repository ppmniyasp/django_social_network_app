# Generated by Django 4.2.6 on 2023-10-23 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_delete_userprofilemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='read_status',
            field=models.BooleanField(default=False),
        ),
    ]