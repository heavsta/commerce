# Generated by Django 3.2.9 on 2021-11-13 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
