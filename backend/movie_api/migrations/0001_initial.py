# Generated by Django 4.2.2 on 2023-06-18 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.PositiveSmallIntegerField()),
                ('rated', models.PositiveSmallIntegerField()),
                ('date_released', models.DateField()),
                ('genre', models.CharField(max_length=255)),
                ('runtime', models.PositiveSmallIntegerField()),
                ('director', models.CharField(max_length=255)),
                ('actors', models.CharField(max_length=255)),
                ('plot', models.TextField()),
                ('poster', models.URLField()),
                ('imdb_rating', models.FloatField()),
                ('imdb_id', models.CharField(max_length=20, unique=True)),
            ],
        ),
    ]