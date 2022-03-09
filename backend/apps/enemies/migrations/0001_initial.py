# Generated by Django 3.2.8 on 2022-03-05 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('damage', models.IntegerField(default=0)),
                ('hp', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='enemies/')),
                ('shield', models.BooleanField(default=False)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enemies', to='core.color')),
                ('faction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enemies', to='core.faction')),
            ],
        ),
        migrations.CreateModel(
            name='EnemyLeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='enemy_leaders/')),
                ('passive', models.BooleanField(default=False)),
                ('hp', models.IntegerField(default=0)),
                ('damage_once', models.IntegerField(blank=True, default=0, null=True)),
                ('damage_per_turn', models.IntegerField(blank=True, default=0, null=True)),
                ('heal_self_per_turn', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnemyLeaderAbility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('starting_enemies_number', models.IntegerField(default=3)),
                ('difficulty', models.CharField(choices=[('easy', 'easy'), ('normal', 'normal'), ('hard', 'hard')], max_length=20)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LevelEnemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enemy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l', to='enemies.enemy')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='l', to='enemies.level')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='enemies',
            field=models.ManyToManyField(related_name='levels', through='enemies.LevelEnemy', to='enemies.Enemy'),
        ),
        migrations.AddField(
            model_name='level',
            name='enemy_leader',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='levels', to='enemies.enemyleader'),
        ),
        migrations.AddField(
            model_name='enemyleader',
            name='ability',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='enemy_leaders', to='enemies.enemyleaderability'),
        ),
        migrations.AddField(
            model_name='enemyleader',
            name='faction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enemy_leaders', to='core.faction'),
        ),
        migrations.AddField(
            model_name='enemy',
            name='move',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enemies', to='enemies.move'),
        ),
    ]
