# Generated by Django 3.2.8 on 2021-11-27 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='id_number',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='student',
            name='semester',
            field=models.CharField(choices=[('First', 'First'), ('Second', 'Second')], max_length=50, null=True),
        ),
    ]
