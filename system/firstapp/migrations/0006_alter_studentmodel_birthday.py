# Generated by Django 3.2.9 on 2022-01-02 06:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_auto_20220102_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmodel',
            name='birthday',
            field=models.DateField(default=datetime.datetime(2022, 1, 2, 6, 37, 54, 23927, tzinfo=utc), verbose_name='день рождения'),
        ),
    ]
