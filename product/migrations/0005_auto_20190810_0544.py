# Generated by Django 2.1.8 on 2019-08-10 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20190810_0542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotion',
            old_name='discount',
            new_name='discount_as_percentag',
        ),
    ]
