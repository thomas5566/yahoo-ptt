from django.db import models
from datetime import date


class Movie(models.Model):
    title = models.CharField("Title", max_length=255, unique=True)
    critics_consensus = models.TextField("Consensus", blank=True)
    release_date = models.DateField('Release_date', default=date.today)
    last_modified = models.DateTimeField('Last_modified', auto_now=True)
    duration = models.CharField("Duration", max_length=255, blank=True)
    genre = models.CharField("Genre", max_length=255, blank=True)
    rating = models.DecimalField(
        "rating", max_digits=3, decimal_places=2, blank=True)
    images = models.ImageField("Images", blank=True)
    amount_reviews = models.CharField(
        "Amount_reviews", max_length=255, blank=True)
    approval_percentage = models.PositiveIntegerField(
        "Porcentae", blank=True, null=True)

    def __str__(self):
        return self.title


class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, default=None, on_delete=models.DO_NOTHING)
    images = models.ImageField(upload_to="yahoo/")

    def __str__(self):
        return self.movie.title


class PttMovie(models.Model):
    author = models.CharField("Author", max_length=255, blank=True)
    contenttext = models.TextField("Contenttext", blank=True)
    date = models.CharField("Date", max_length=255, blank=True)
    title = models.CharField("Title", max_length=255, blank=True)
    key_word = models.ForeignKey(
        Movie, on_delete=models.DO_NOTHING, related_name="comments")

    def __str__(self):
        return self.title
