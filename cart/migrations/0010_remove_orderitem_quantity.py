# Generated by Django 5.0.7 on 2024-08-04 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0009_orderitem"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="quantity",
        ),
    ]
