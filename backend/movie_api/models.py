from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=25)
    released = models.CharField(max_length=50,null=True)
    runtime = models.CharField(max_length=50)
    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255,null=True)
    writer = models.CharField(max_length=255,null=True)
    actors = models.CharField(max_length=255,null=True)
    plot = models.TextField()
    language = models.CharField(max_length=255,null=True)
    country = models.CharField(max_length=255,null=True)
    awards = models.CharField(max_length=255,null=True)
    poster = models.URLField()
    ratings = models.JSONField(null=True)
    metascore = models.CharField(max_length=50,null=True)
    imdb_rating = models.FloatField()
    imdb_votes = models.CharField(max_length=50,null=True)
    imdb_id = models.CharField(max_length=20, unique=True)
    movie_type = models.CharField(max_length=50,null=True)
    dvd = models.CharField(max_length=50,null=True)
    box_office = models.CharField(max_length=50,null=True)
    production = models.CharField(max_length=255,null=True)
    website = models.URLField(null=True)
    response = models.CharField(max_length=10,null=True)
    
    def __str__(self):
        return self.title
