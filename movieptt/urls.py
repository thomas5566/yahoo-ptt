from django.urls import path, include
from movieptt import views

from rest_framework.routers import DefaultRouter

from movieptt import views


router = DefaultRouter()
router.register('movies-viewset', views.MovieViewSet,
                basename='movies-viewset')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
