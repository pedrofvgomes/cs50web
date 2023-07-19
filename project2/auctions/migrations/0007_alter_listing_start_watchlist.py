# Generated by Django 4.2.3 on 2023-07-18 23:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_bid_amount_alter_listing_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 19, 0, 25, 44, 865362)),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
