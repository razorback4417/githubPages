# Generated by Django 3.0.8 on 2020-12-28 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsConnect', '0006_auto_20201228_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
