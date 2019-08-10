# Generated by Django 2.1.8 on 2019-08-10 05:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_subproductimage_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='discount_as_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='promotion',
            name='end_date_discount',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 8, 10, 5, 42, 48, 214368, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promotion',
            name='start_date_discount',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 8, 10, 5, 42, 55, 569169, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
