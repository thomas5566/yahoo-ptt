import sys
import logging
sys.path.append("..")

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.twisted import TwistedScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from crawlmovie.spiders.yahoomovie import YahoomovieSpider # daily
from crawlmovie.spiders.ptt_movies import PttMoviesSpider # daily
from crawlmovie.filter import FilterAndInsertData # when YahoomovieSpider PttMoviesSpider mission completed, execute

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)

trigger1 = OrTrigger([
    CronTrigger(hour='22', minute='30'),
])

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
# scheduler.add_job(process.crawl, 'cron', args=[YahoomovieSpider], hour='22', minute='30')
# scheduler.add_job(process.crawl, 'cron', args=[PttMoviesSpider], hour='22', minute='30')
scheduler.add_job(YahoomovieSpider, trigger=trigger1)
scheduler.start()
process.start(False)
