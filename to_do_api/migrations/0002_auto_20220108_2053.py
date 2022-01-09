# Generated by Django 3.2.9 on 2022-01-08 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('pk',)},
        ),
        migrations.AlterField(
            model_name='task',
            name='completed_date',
            field=models.DateTimeField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 8, 20, 53, 12, 41833)),
        ),
    ]
