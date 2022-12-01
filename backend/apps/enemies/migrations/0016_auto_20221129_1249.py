# Generated by Django 3.2.8 on 2022-11-29 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enemies', '0015_auto_20221129_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='enemy',
            name='base_hp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='enemy',
            name='deathwish_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='enemy',
            name='default_timer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='enemy',
            name='reset_timer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='enemy',
            name='timer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='enemy',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
