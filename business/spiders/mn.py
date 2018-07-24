# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin


class MnSpider(scrapy.Spider):
    name = 'mn'
    allowed_domains = ['coderbusy.com']
    start_urls = ['https://proxy.coderbusy.com/classical/country/cn.aspx']

    def parse(self, response):

        print("abc"*10)
        tr_list = response.xpath("//div[@class='table-responsive']/table/tbody/tr")
        for tr in tr_list:
            item = {}
            item["ip"] = tr.xpath("./td[@class='port-box']/@data-ip").extract_first()
            item["port"] = tr.xpath("./td[@class='port-box']/text()").extract_first()
            item["cate"] = tr.xpath("./td[8]/a/text()").extract_first()
            item["times"] = tr.xpath("./td[11]/text()").extract_first()

            if item["cate"] == "高匿":
                yield item
                print(item)

        next_url = response.xpath("//li[@title='下一页']/a/@href").extract_first()

        if next_url:
            next_url = urljoin(response.url,next_url)
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )







