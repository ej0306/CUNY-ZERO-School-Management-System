# Generated by Django 3.2.8 on 2021-12-04 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_reviewclasses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classes',
            name='class_id',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
