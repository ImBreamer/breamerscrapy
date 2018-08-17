# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib.request

import pymysql
from scrapy.conf import settings


class BreamerscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class DemoPipeline(object):
    def process_item(self, item, spider):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        # res = urllib.request.urlopen('', headers=headers)
        file_name = os.path.join('C:/Users/23769/Desktop/wb', item['title'] + '.pdf')
        # os.path.join将多个路径组合后返回
        urllib.request.urlretrieve(item['link'], file_name)


class NewsPipeline(object):
    def process_item(self, item, spider):
        db_client = pymysql.connect(host=settings['MYSQL_HOST'],
                                    user=settings['MYSQL_USER'],
                                    password=settings['MYSQL_PASSWD'],
                                    db=settings['MYSQL_DBNAME'],
                                    charset=settings['MYSQL_CHARSET'])
        cursor = db_client.cursor()
        sql = "INSERT INTO app_news " \
              "(id,title,create_time,outline,keyword,title_img,content,content_img,from_link) " \
              "VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
              % (int(item['id']), item['title'], item['time'], item['outline'], item['keyword'],
                 item['title_img'], item['content'], item['content_img'], item['from_link'])
        cursor.execute(sql)
        db_client.commit()


class WhiteBookPipeline(object):
    def process_item(self, item, spider):
        db_client = pymysql.connect(host=settings['MYSQL_HOST'],
                                    user=settings['MYSQL_USER'],
                                    password=settings['MYSQL_PASSWD'],
                                    db=settings['MYSQL_DBNAME'],
                                    charset=settings['MYSQL_CHARSET'])
        cursor = db_client.cursor()
        sql = "INSERT INTO app_white_book " \
              "(title,create_time,content,write_unit) VALUES ('%s', '%s', '%s', '%s')" \
              % (item['title'], item['create_time'], item['content'], item['write_unit'])
        cursor.execute(sql)
        db_client.commit()
