# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BreamerscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DemoItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()


class NewsItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    outline = scrapy.Field()
    keyword = scrapy.Field()
    title_img = scrapy.Field()
    content = scrapy.Field()
    content_img = scrapy.Field()
    from_link = scrapy.Field()


class WhiteBookItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    create_time = scrapy.Field()
    content = scrapy.Field()
    write_unit = scrapy.Field()
    hot = scrapy.Field()
    thumbnail = scrapy.Field()
