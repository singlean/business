# -*- coding: utf-8 -*-
import scrapy


class RsSpider(scrapy.Spider):
    name = 'rs'
    allowed_domains = ['fang.com']
    start_urls = ['http://esf.wuhan.fang.com/']

    def parse(self, response):
        pass
