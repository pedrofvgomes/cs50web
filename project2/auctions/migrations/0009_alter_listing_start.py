# Generated by Django 4.2.3 on 2023-07-19 00:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_start_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 1, 55, 42, 971540)),
        ),
    ]