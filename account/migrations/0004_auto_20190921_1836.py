# Generated by Django 2.2.5 on 2019-09-21 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190921_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='status_is_active',
            field=models.BooleanField(default=True),
        ),
    ]
