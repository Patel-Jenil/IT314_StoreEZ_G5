# Generated by Django 4.2.7 on 2023-11-20 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_booking_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='latitude',
            field=models.FloatField(default=23.1862737352),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='longitude',
            field=models.FloatField(default=72.6283225558),
        ),
    ]
