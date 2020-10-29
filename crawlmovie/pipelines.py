from datetime import datetime
from time import strftime
from itemadapter import ItemAdapter
import scrapy
import os
import re

from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from scrapy.exceptions import DropItem

# Scrapy export csv without specifying in cmd
from scrapy import signals
from scrapy.exporters import CsvItemExporter, JsonItemExporter
import csv


from movieptt.models import Movie


def clean_title(param):
    # regex = "[A-Za-z\/\[\]\.\']+"
    # regex = "[^\u4e00-\u9fa5]+"
    # param = re.sub(regex, " ", str(param))
    return "".join(param)


def clean_critics_consensus(param):
    return "".join(param)


def clean_date(param):
    # try:
    regex = "[^0-9]+"
    param = re.sub(regex, "", str(param))
    param = datetime.strptime(param, "%Y%m%d").strftime("%Y-%m-%d")
    return param
    # except ValueError:
    #     # regex = "[^0-9]+"
    #     # param = re.sub(regex, "", str(param))
    #     param = datetime.strptime(param, "%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d %H%M")
    #     return param


def clean_duration(param):
    try:
        return "".join(param.split())
    except:
        return "".join(param)


def clean_genre(param):
    return "".join(param)


def clean_rating(param):
    return "".join(param)


def clean_images(param):
    if param:
        try:
            param = param[0]["path"]
        except TypeError:
            pass
    return param


def clean_amount_reviews(param):
    regex = "[^A-Za-z0-9]+"
    param = re.sub(regex, "", str(param))
    return "".join(param)


def clean_author(param):
    return "".join(param)


def clean_contenttext(param):
    return "".join(param)


class PttPipeline:
    def process_item(self, item, spider):
        item["title"] = clean_title(item["title"])
        item["author"] = clean_author(item["author"])
        item["date"] = item["date"]
        item["contenttext"] = clean_contenttext(item["contenttext"])

        return item


class YahooPipeline:
    def process_item(self, item, spider):
        item["title"] = clean_title(item["title"])
        item["date"] = clean_date(item["date"])
        item["critics_consensus"] = clean_critics_consensus(
            item["critics_consensus"])
        item["duration"] = clean_duration(item["duration"])
        item["genre"] = clean_genre(item["genre"])
        item["rating"] = clean_rating(item["rating"])
        item["images"] = clean_images(item["images"])
        item["amount_reviews"] = clean_amount_reviews(item["amount_reviews"])

        try:
            Movie.objects.create(
                title=item["title"],
                release_date=item["date"],
                critics_consensus=item["critics_consensus"],
                duration=item["duration"],
                genre=item["genre"],
                rating=item["rating"],
                images=item["images"],
                amount_reviews=item["amount_reviews"],
            )
        except:
            print("The movie information is already exists!!")

        return item


class CustomImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # for (image_url, image_name) in zip(item['images'], item['title']):
        #     yield scrapy.Request(url=image_url, meta={"image_name": image_name})
        if "images" in item:
            for img_name, image_url in item["images"].items():
                request = scrapy.Request(url=image_url)
                new_img_name = ("%s.jpg" % (img_name)).replace(" ", "")
                request.meta["img_name"] = new_img_name
                yield request

    def file_path(self, request, response=None, info=None):
        return os.path.join(info.spider.IMAGE_DIR, request.meta["img_name"])


class DeleteNullTitlePipeline(object):
    def process_item(self, item, spider):
        title = item["title"]
        if title:
            return item
        else:
            raise DropItem("found null title %s", item)


class DuplicatesTitlePipeline(object):
    def __init__(self):
        self.movie = set()

    def process_item(self, item, spider):
        title = item["title"]
        if title in self.movie:
            raise DropItem("duplicates title found %s", item)
        self.movie.add(title)
        return item


class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        # self.exporter.fields_to_export = ['title', 'critics_consensus', 'date',
        #                                   'duration', 'genre', 'rating', 'amount_reviews', 'images']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
