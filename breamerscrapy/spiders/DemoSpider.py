import re

import scrapy

from breamerscrapy.items import DemoItem


class DemoSider(scrapy.Spider):
    name = "aii-alliance"
    allowed_domains = ["aii-alliance.org"]
    start_urls = ["http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23",
                  "http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=2",
                  "http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=3"]

    def parse(self, response):
        files = response.xpath('//ul[@class="Meeting_box"]/a')
        for file in files:
            link = file.xpath('./@href').extract_first()
            # item['desc'] = re.search('[1-9]\d{3}.(0[1-9]|1[0-2]).(0[1-9]|[1-2][0-9]|3[0-1])',
            #                          file.xpath('./li/div[@class="Meeting_box_time"]').extract_first()).group()
            yield scrapy.Request(link, callback=self.url_parse)

    def url_parse(self, response):
        item = DemoItem()
        item['title'] = response.xpath('//h2[@class="inside_content_title"]/text()').extract_first()
        item['link'] = 'http://www.aii-alliance.org/' + response.xpath('//div[@class="news-content"]/a/@href').extract_first()
        yield item
