# Generated by Django 2.1.8 on 2019-08-14 07:24

import customer.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0011_auto_20190813_0644'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('full_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(blank=True, max_length=50)),
                ('email', models.CharField(blank=True, max_length=255)),
                ('address', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_status', models.BooleanField(default=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Location')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='SaleInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, default=customer.models.increment_invoice_number, max_length=500, null=True, validators=[django.core.validators.RegexValidator(code='Number is invalide', message='Produce number must be Alphanumeric', regex='^[a-zA-Z0-9]*$')])),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_status', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_customer', to='customer.Customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='SaleInvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(blank=True, default=0.0)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_status', models.BooleanField(default=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice', to='customer.SaleInvoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_item_product', to='product.Product')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='SaleInvoiceItemHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(default=0.0)),
                ('description', models.TextField(blank=True)),
                ('action', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_status', models.BooleanField(default=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_history', to='customer.SaleInvoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_invoice_item_product_history', to='product.Product')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
    ]
