# Generated by Django 5.0.7 on 2024-07-31 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adminsite", "0008_maincategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="maincategory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="adminsite.maincategory",
            ),
        ),
    ]
