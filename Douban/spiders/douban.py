# -*- coding: utf-8 -*-
import re
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Douban.items import MovieItemLoader, MovieMessagesItem
from Douban.utils.spider_re import production_country_re, language_re
from Douban.settings import SQL_DATETIME_FORMAT

class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    rules = (
        Rule(LinkExtractor(allow=r'chart'), follow=True),
        Rule(LinkExtractor(allow=r'celebrity/\d+'), follow=True),
        Rule(LinkExtractor(allow=r'subject/\d+/?from=.*?'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'subject/\d+/$'), callback='parse_item', follow=True),

    )

    def parse_item(self, response):
        item_loader = MovieItemLoader(item=MovieMessagesItem(), response=response)
        item_loader.add_value('movie_url', response.url)
        item_loader.add_xpath('name', '//*[@id="content"]/h1/span[1]/text()')
        item_loader.add_xpath('director', '//*[@id="info"]/span[1]/span[2]/a/text()')
        item_loader.add_css('actor', 'a[rel="v:starring"]::text')
        item_loader.add_css('movie_type', 'span[property="v:genre"]::text')
        item_loader.add_value('production_country', production_country_re(response.text))
        item_loader.add_value('language', language_re(response.text))
        item_loader.add_css('release_data', 'span[property="v:initialReleaseDate"]::text')
        item_loader.add_css('length', 'span[property="v:runtime"]::text')
        item_loader.add_xpath('score', '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        item_loader.add_xpath('number_of_comments', '//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')
        item_loader.add_xpath('top_rank', '//*[@id="content"]/div[1]/span[1]/text()')
        item_loader.add_value('crawl_time', datetime.now().strftime(SQL_DATETIME_FORMAT))

        m_item = item_loader.load_item()
        yield m_item
