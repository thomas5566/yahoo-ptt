from django.db import models


class Movie(models.Model):
    title = models.CharField("title", max_length=255, unique=True)
    critics_consensus = models.TextField("Consensus", blank=True, null=True)
    date = models.CharField("date", max_length=255, blank=True, null=True)
    duration = models.CharField("duration", max_length=255, blank=True, null=True)
    genre = models.CharField("genre", max_length=255, blank=True, null=True)
    rating = models.DecimalField(
        "rating", max_digits=3, decimal_places=2, blank=True, null=True
    )
    images = models.ImageField(
        "images", upload_to="movie/images/", blank=True, null=True
    )
    amount_reviews = models.CharField(
        "amount_reviews", max_length=255, blank=True, null=True
    )
    approval_percentage = models.PositiveIntegerField(
        "Porcentae", blank=True, null=True
    )

    def __str__(self):
        return self.title


class PttMovie(models.Model):
    author = models.CharField("Author", max_length=255, blank=True, null=True)
    contenttext = models.TextField("Contenttext", blank=True, null=True)
    date = models.CharField("Date", max_length=255, blank=True, null=True)
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    key_word = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.title
