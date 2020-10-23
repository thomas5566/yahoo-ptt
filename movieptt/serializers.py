from django.db.models import fields
from rest_framework import serializers
from movieptt.models import Movie
from django.utils.timezone import now


class MovieSerializer(serializers.ModelSerializer):
    # release_date = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ('id', 'title', 'release_date')

    # def get_day_since_created(self, obj):
    #     return (now() - obj.release_date).days
