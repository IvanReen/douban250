# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings


class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class MySqlPipeline(object):
    def __init__(self):
        setting = get_project_settings()
        self.host = setting['DB_HOST']
        self.port = setting['DB_PORT']
        self.user = setting['DB_USER']
        self.pwd = setting['DB_PWD']
        self.name = setting['DB_NAME']
        self.charset = setting['DB_CHARSET']

        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, password=self.pwd, user=self.user, database=self.name, charset=self.charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'insert into movie_list (img_url, movie_name, comment, movie_content, leadings, imdb_url) values ("%s", "%s", "%s", "%s", "%s", "%s")' % (item["img_url"], item["movie_name"], item["comment"], item["movie_content"], item["leadings"], item["imdb_url"])
        self.cursor.execute(sql)
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
        self.cursor.close()