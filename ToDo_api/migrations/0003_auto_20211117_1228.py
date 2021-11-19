# Generated by Django 3.2.9 on 2021-11-17 12:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_api', '0002_alter_task_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 17, 12, 28, 27, 29212)),
        ),
    ]
