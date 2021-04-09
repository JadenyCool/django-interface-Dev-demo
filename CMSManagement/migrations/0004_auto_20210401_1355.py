# Generated by Django 3.1.7 on 2021-04-01 05:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMSManagement', '0003_auto_20210331_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='authToken',
            fields=[
                ('key', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('create', models.DateTimeField(default=datetime.datetime(2021, 4, 1, 13, 55, 46, 782223))),
                ('user_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='phonemanage',
            name='is_home',
            field=models.IntegerField(choices=[('借出', 1), ('在库', 0)]),
        ),
    ]