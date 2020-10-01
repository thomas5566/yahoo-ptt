import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawlmovie.items import ScrapyCloudItem


class PttMoviesSpider(CrawlSpider):
    name = 'ptt_movies'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/movie/index.html']

    # custom_settings = {
    #     'DOWNLOAD_DELAY': 3,
    #     "ITEM_PIPELINES": {
    #         'scrapy_cloud.pipelines.PttPipeline': 100,
    #         'scrapy_cloud.pipelines.DeleteNullTitlePipeline': 200,
    #         'scrapy_cloud.pipelines.DuplicatesTitlePipeline': 200,
    #     },
    #     'AUTOTHROTTLE_ENABLED': True,
    #     # The initial download delay
    #     'AUTOTHROTTLE_START_DELAY': 5,
    #     # The maximum download delay to be set in case of high latencies
    #     'AUTOTHROTTLE_MAX_DELAY': 60,
    #     # The average number of requests Scrapy should be sending in parallel to
    #     # each remote server
    #     'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
    #     # "CLOSESPIDER_ITEMCOUNT": 150,
    # }

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='title']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(
            restrict_xpaths="//div[@class='btn-group btn-group-paging']/a[2]"))
    )

    def parse_item(self, response):
        item = ScrapyCloudItem()
        # item['title'] = response.xpath(
        #     "normalize-space((//span[@class='article-meta-value'])[3]/text())").extract()
        # i['title'] = ''.join(title)
        for s in response.xpath("normalize-space((//span[@class='article-meta-value'])[3]/text())").extract():
            if "雷" in s:
                item['title'] = s

                item['author'] = response.xpath(
                    "(//span[@class='article-meta-value'])[1]/text()").extract()
                # i['author'] = ''.join(author)

                item['date'] = response.xpath(
                    "(//span[@class='article-meta-value'])[4]/text()").extract()
                # i['date'] = ''.join(date)

                item['contenttext'] = response.xpath(
                    "//div[@id='main-content']/text()").extract()

                yield item

            else:
                yield None
