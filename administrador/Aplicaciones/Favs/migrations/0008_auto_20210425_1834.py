# Generated by Django 3.2 on 2021-04-25 18:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Favs', '0007_auto_20210424_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritos',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 25, 18, 34, 47, 960604, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='lista',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 25, 18, 34, 47, 961372, tzinfo=utc)),
        ),
    ]