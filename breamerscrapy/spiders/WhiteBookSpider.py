import re

import scrapy

from breamerscrapy.items import WhiteBookItem


class WhiteBookSpider(scrapy.Spider):
    name = "whitebook"
    allowed_domains = ["aii-alliance.org"]
    start_urls = ["http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23",
                  "http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=2",
                  "http://www.aii-alliance.org/index.php?m=content&c=index&a=lists&catid=23&page=3"]

    def parse(self, response):
        item = WhiteBookItem()
        files = response.xpath('//ul[@class="Meeting_box"]/a')
        for file in files:
            link = file.xpath('./@href').extract_first()
            item['create_time'] = re.search('[1-9]\d{3}.(0[1-9]|1[0-2]).(0[1-9]|[1-2][0-9]|3[0-1])',
                                     file.xpath('./li/div[@class="Meeting_box_time"]').extract_first()).group()
            yield scrapy.Request(link, meta={'item': item}, callback=self.url_parse)

    def url_parse(self, response):
        item = response.meta['item']
        content_str = ""
        write_unit_str = ""
        content_div = response.xpath('//div[@class="inside_content_text"]//span/descendant::text()').extract()
        if len(content_div) > 0:
            write_unit_str, content_str = self.check_content(content_str, content_div)
        else:
            conten_strs = response.xpath('//div[@class="inside_content_text"]/text()').extract()
            write_unit_str, content_str = self.check_content(content_str, conten_strs)
        item['title'] = response.xpath('//h2[@class="inside_content_title"]/text()').extract_first()
        item['content'] = content_str
        item['write_unit'] = write_unit_str
        yield item

    def check_content(self, c, x):
        s = 0
        t_str = ""
        for secspan_text in x:
            p_str = secspan_text.strip()
            if s == 0:
                if p_str.find("编写单位") == -1:
                    c = c + p_str + '\n'
                else:
                    if p_str.find("牵头编写单位") > -1:
                        t_str_s = p_str.split('：')
                        if len(t_str_s) < 2:
                            s = 3
                        else:
                            t_str = p_str.split('：')[1]
                            s = 2
                    else:
                        s = 1
            elif s == 1:
                if p_str.find("牵头编写单位") > -1:
                    t_str = p_str.split('：')[1]
                    s = 2
            elif s == 3:
                t_str = p_str.split('：')[1]
                s = 2
            else:
                break
        if t_str == "":
            t_str = "工业互联网产业联盟"
        return t_str, c
