# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Compose


def set_default_value(value):
    # 如果没有取到值，则设置默认值
    # 主要针对字符串类型数据
    if value:
        return value
    else:
        return ['null']


def set_default_num_value(value):
    # 如果没有取到值，则设置默认值
    # 主要针对数值类型数据
    if value:
        return value
    else:
        return [0]


def return_value(value):
    return value


def conversion_format(value):
    return '/'.join(i for i in value)


def top_rank_default(value):
    if value:
        return [re.match('No.(\d+)', value[0]).group(1)]
    else:
        return [0]


def re_me(value):
    if value:
        try:
            length = re.search('(\d+).*?', value[0]).group(1)
            return length
        except:
            return 0


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()
    default_input_processor = set_default_value


class MovieMessagesItem(scrapy.Item):
    movie_url = scrapy.Field()
    crawl_time = scrapy.Field()
    name = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field(
        # output_processor=conversion_format
        output_processor=conversion_format
    )
    movie_type = scrapy.Field(
        output_processor=conversion_format
    )
    production_country = scrapy.Field()
    language = scrapy.Field()
    release_data = scrapy.Field()
    length = scrapy.Field(
        input_processor=set_default_num_value,
        output_processor=re_me
    )
    score = scrapy.Field(
        input_processor=set_default_num_value
    )
    number_of_comments = scrapy.Field(
        input_processor=set_default_num_value
    )
    top_rank = scrapy.Field(
        input_processor=top_rank_default
    )

    # def to_insert_mysql(self):
    #     params = (
    #         self['movie_url'], self['crawl_time'], self['name'], self['director'], self['actor'], self['movie_type'],
    #         self['production_country'], self['language'], self['release_data'], int(self['length']), float(self['score']),
    #         int(self['number_of_comments'], self['top_rank'])
    #     )
    #     sql = """INSERT INTO douban_movie (movie_url, crawl_time, name, director, actor, movie_type, production_country, language,
    #           release_data, length, score, number_of_comments, top_rank)
    #           values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #           ON DUPLICATE key  update  number_of_comments=values(number_of_comments), top_rank=values(top_rank), score=values(score)"""
    #
    #     return sql, params

