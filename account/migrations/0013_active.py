# Generated by Django 2.2.6 on 2020-04-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20191113_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='active',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=200, unique=True)),
                ('active', models.CharField(max_length=2)),
            ],
        ),
    ]