# -*- coding: utf-8 -*-
import scrapy


class KfdlSpider(scrapy.Spider):
    name = 'kfdl'
    allowed_domains = ['kuaidaili.com']
    start_urls = ["https://www.kuaidaili.com/ops/proxylist/{}/".format(i) for i in range(1,11)]
    # start_urls = ['https://www.kuaidaili.com/ops/proxylist/1/']

    def parse(self, response):

        # 每页代理列表
        tr_list = response.xpath("//div[@id='freelist']//tbody/tr")
        for tr in tr_list:
            item = {}
            item["ip"] = tr.xpath("./td[1]/text()").extract_first()
            item["port"] = tr.xpath("./td[2]/text()").extract_first()
            item["cate"] = tr.xpath("./td[3]/text()").extract_first()
            item["http"] = tr.xpath("./td[4]/text()").extract_first()
            item["response_time"] = tr.xpath("./td[7]/text()").extract_first()



            yield item




















