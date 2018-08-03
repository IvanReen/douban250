# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    img_url = scrapy.Field()
    movie_name = scrapy.Field()
    comment = scrapy.Field()
    movie_content = scrapy.Field()
    leadings = scrapy.Field()
    imdb_url = scrapy.Field()
