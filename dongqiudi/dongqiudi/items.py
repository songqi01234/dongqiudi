# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DongqiudiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    times = scrapy.Field()
    author = scrapy.Field()
    img = scrapy.Field()
    news = scrapy.Field()
    url = scrapy.Field()
