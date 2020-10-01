from django.contrib import admin
from .models import Movie, PttMovie
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, MovieAdmin)


class PttMovieAdmin(admin.ModelAdmin):
    pass


admin.site.register(PttMovie, PttMovieAdmin)
