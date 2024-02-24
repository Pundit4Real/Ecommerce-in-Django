# Generated by Django 5.0.1 on 2024-02-22 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='core.product'),
        ),
    ]