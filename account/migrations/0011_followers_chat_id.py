# Generated by Django 2.2.6 on 2019-10-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_remove_followers_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='followers',
            name='chat_id',
            field=models.CharField(default=None, max_length=200, unique=True),
        ),
    ]
