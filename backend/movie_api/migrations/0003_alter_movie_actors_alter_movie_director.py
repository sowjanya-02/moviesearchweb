# Generated by Django 4.2.2 on 2023-06-19 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_api', '0002_remove_movie_date_released_movie_awards_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
