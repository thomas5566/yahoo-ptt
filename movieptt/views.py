from django.http import request
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from .models import Movie
from .models import PttMovie


def home(request):
    all_rows = Movie.objects.all()
    movies = [
        all_rows.filter(title=item["title"]).last()
        for item in Movie.objects.values("title")
        .distinct()
        .order_by("rating")
        .reverse()
    ]
    return render(request, "movies/home.html", {"movies": movies})


def detail(request, movie_pk):
    detail = get_object_or_404(Movie, pk=movie_pk)
    return render(request, "movies/detail.html", {"detail": detail})


def comments(request, comments):
    movies = [m.title for m in Movie.objects.all()]
    if comments in movies:
        match_comments = PttMovie.objects.filter(comments__title=comments)
        return render(request, "movies/detail.html", {"comments": match_comments})
