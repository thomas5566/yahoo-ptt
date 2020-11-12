from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawlmovie.spiders.ptt_movies import PttMoviesSpider
from crawlmovie.spiders.yahoomovie import YahoomovieSpider


process = CrawlerProcess(get_project_settings())
process.crawl(YahoomovieSpider)
process.crawl(PttMoviesSpider)
process.start()