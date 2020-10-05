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

    context = {
        'movies': movies
    }
    return render(request, "movies/home.html", context)


def detail(request, movie_pk):
    detail = get_object_or_404(Movie, pk=movie_pk)
    movies = Movie.objects.get(pk=movie_pk)
    context = {
        'detail': detail,
        'movies': movies
    }

    return render(request, "movies/detail.html", context)


# def comments(request, movie_pk):
#     movies = Movie.objects.all().values()

#     comments = movies.objects.filter(comments_title='天能')

#     # comments = PttMovie.objects.filter(comments=request.title)
#     context = {
#         'comments': comments,
#     }
#     return render(request, "movies/detail.html", context)
