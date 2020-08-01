# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

from Douban.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT

class DoubanPipeline:
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline:
    # 异步
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted 使mysql插入异步化
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        #处理异步出现的错误
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
         params = (
            item['movie_url'], item['crawl_time'], item['name'], item['director'], item['actor'], item['movie_type'],
            item['production_country'], item['language'], item['release_data'], int(item['length']), float(item['score']),
            int(item['number_of_comments']), int(item.get('top_rank', 0))
         )

         sql = """INSERT INTO douban_movie (movie_url, crawl_time, name, director, actor, movie_type, production_country, language,
                      release_data, length, score, number_of_comments, top_rank)
                      values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                      ON DUPLICATE key  update  number_of_comments=values(number_of_comments), top_rank=values(top_rank), score=values(score)"""

         cursor.execute(sql, params)