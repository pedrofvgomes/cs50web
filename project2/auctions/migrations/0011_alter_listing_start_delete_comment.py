# Generated by Django 4.2.3 on 2023-07-19 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_open_alter_listing_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 19, 32, 45, 165208)),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]