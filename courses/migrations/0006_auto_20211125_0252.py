# Generated by Django 3.2.8 on 2021-11-25 02:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_classes_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='credit',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classes',
            name='current_capacity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classes',
            name='days_and_time',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='classes',
            name='end_date',
            field=models.DateField(default=datetime.date(1, 1, 1), null=True),
        ),
        migrations.AddField(
            model_name='classes',
            name='full_capacity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classes',
            name='start_date',
            field=models.DateField(default=datetime.date(1, 1, 1), null=True),
        ),
    ]