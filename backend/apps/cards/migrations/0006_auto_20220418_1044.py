# Generated by Django 3.2.8 on 2022-04-18 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_auto_20220402_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='locked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='leader',
            name='locked',
            field=models.BooleanField(default=True),
        ),
    ]
