# Generated by Django 2.2.6 on 2019-10-03 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20191003_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followers',
            name='chat_id',
        ),
    ]
