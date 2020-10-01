# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from movieptt.models import Movie
from movieptt.models import PttMovie


class ScrapyCloudItem(scrapy.Item):
    django_model = PttMovie
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    contenttext = scrapy.Field()


class YahooCloudItem(scrapy.Item):
    django_model = Movie
    title = scrapy.Field()
    critics_consensus = scrapy.Field()
    date = scrapy.Field()
    duration = scrapy.Field()
    genre = scrapy.Field()
    rating = scrapy.Field()
    amount_reviews = scrapy.Field()
    images = scrapy.Field()
