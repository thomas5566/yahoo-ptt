from django.contrib import admin
from .models import Movie, PttMovie, MovieImage
# Register your models here.


class MovieImageAdmin(admin.StackedInline):
    model = MovieImage


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieImageAdmin]

    class Meta:
        model = Movie


@admin.register(MovieImage)
class MovieImageAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Movie, MovieAdmin)


class PttMovieAdmin(admin.ModelAdmin):
    pass


admin.site.register(PttMovie, PttMovieAdmin)
