# Generated by Django 3.2.7 on 2021-11-20 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_quantity',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
