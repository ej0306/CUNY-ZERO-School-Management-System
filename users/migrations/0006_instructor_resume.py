# Generated by Django 3.2.8 on 2021-11-14 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211112_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='resume',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]