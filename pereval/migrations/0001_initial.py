# Generated by Django 5.2.1 on 2025-05-19 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(max_length=255, null=True)),
                ('summer', models.CharField(max_length=255, null=True)),
                ('autumn', models.CharField(max_length=255, null=True)),
                ('spring', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('fam', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('otc', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Pereval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('other_titles', models.CharField(max_length=255)),
                ('connect', models.CharField(max_length=255, null=True)),
                ('add_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('new', 'новый'), ('pending', 'в работе'), ('accepted', 'принят'), ('rejected', 'не принят')], max_length=20)),
                ('coords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.coords')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval.user')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.URLField()),
                ('title', models.CharField(max_length=255)),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pereval.pereval')),
            ],
        ),
    ]
