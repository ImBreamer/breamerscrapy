import re
import time

import pymysql
import scrapy

from breamerscrapy.items import NewsItem


class NewsScrapy(scrapy.Spider):
    name = "news"
    allowed_domains = ["casicloud.com"]
    start_urls = ["http://www.casicloud.com/news/list"]

    def parse(self, response):
        total_page = re.search('\d+', response.xpath('//span[@class="total total_page"]/text()')
                               .extract_first()).group()
        next_urls = set()
        db_client = pymysql.connect(host='106.74.146.168', user='root', password='root#123QAZ', db='app',
                                    charset='utf8')
        cursor = db_client.cursor()
        sql = "select id from app_news"
        cursor.execute(sql)
        results = cursor.fetchall()
        for s in results:
            next_urls.add(s[0])
        for i in range(0, int(total_page)):
            new_link = 'http://www.casicloud.com/news/list?id=&page=%d' % i
            print(new_link)
            yield scrapy.Request(new_link, meta={'set': next_urls}, callback=self.second_url_parse)

    def second_url_parse(self, response):
        second_urls = response.meta['set']
        news_li = response.xpath('//ul[@class="news_list"]/li')
        for news in news_li:
            item = NewsItem()
            title = news.xpath('./div[@class="right_box"]/div[@class="news_title"]/a/@title').extract_first()
            news_id = re.search('\d+', news.xpath('./div[@class="left_box"]/a/@href').extract_first()).group()
            if title.find("手册") == -1 and int(news_id) not in second_urls:
                new_link = 'http://www.casicloud.com' + news.xpath('./div[@class="left_box"]/a/@href').extract_first()
                item['time'] = news.xpath('./div[@class="right_box"]/div[@class="bottom_btn"]'
                                          '/div[@class="left_link"]/span[@class="time"]/text()').extract_first().strip()
                item['outline'] = news.xpath('./div[@class="right_box"]/div[@class="news_text"]/a/p/text()') \
                    .extract_first().strip()
                item['id'] = news_id
                item['title_img'] = news.xpath('./div[@class="left_box"]/a/img/@src').extract_first()
                item['title'] = title
                yield scrapy.Request(new_link, meta={'set': second_urls, 'item': item}, callback=self.url_parse)

    def url_parse(self, response):
        item = response.meta['item']
        keywords = response.xpath('//div[@class="key_words"]/a')
        ps = response.xpath('//div[@class="content"]/descendant::p[not(@class="desc")]')
        p_iframe = response.xpath('//div[@class="content"]/p/iframe')
        if len(p_iframe) < 1:
            keywords_str = ""
            for keyword in keywords:
                x = keyword.xpath('@title').extract_first()
                if keywords_str == "":
                    keywords_str = x
                else:
                    keywords_str = keywords_str + ',' + x
            p_str = ""
            img_str = ""
            form_link_str = ""
            for p in ps:
                inner = ""
                imgs = p.xpath('./descendant::img')
                if len(imgs) > 0:
                    for img in imgs:
                        if img_str == "":
                            img_str = img.xpath('@src').extract_first()
                            inner = 'img=' + img.xpath('@src').extract_first()
                        else:
                            img_str = img_str + '|' + img.xpath('@src').extract_first()
                            inner = 'img=' + img.xpath('@src').extract_first()
                ases = p.xpath('.//text()').extract()
                for ase in ases:
                    inner = inner + ase.replace("'", "‘").strip().strip('\n')
                p_str = p_str + inner + '<p>'
                if len(ases) > 0 and ases[0].find("来源：") > -1:
                    for ase in ases:
                        form_link_str = form_link_str + ase.replace("'", "‘").strip().strip('\n')
            if form_link_str == "":
                item['from_link'] = '来源： 航天云网'
            else:
                item['from_link'] = form_link_str
            item['content'] = p_str
            item['keyword'] = keywords_str
            item['content_img'] = img_str
            yield item
