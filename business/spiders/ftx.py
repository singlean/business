# -*- coding: utf-8 -*-
import scrapy,re
from scrapy_redis.spiders import RedisSpider
from urllib.parse import urljoin
import pprint


class FTXSpider(RedisSpider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    # start_urls = ['http://zu.wuhan.fang.com/?ctm=1.wuhan.xf_search.head.116']
    redis_key = "ftx"

    def parse(self, response):
        # 租房列表
        dl_list = response.xpath("//div[@class='houseList']/dl")
        # 获取租房信息
        for dl in dl_list:
            item = {}
            item["title"] = dl.xpath(".//p[@class='title']/a/text()").extract_first()
            item["url"] = dl.xpath(".//p[@class='title']/a/@href").extract_first()
            if item["url"]:
                item["url"] = "http://zu.wuhan.fang.com" + item["url"]

                yield scrapy.Request(
                    url=item["url"],
                    callback=self.parse_detail,
                    meta={"item":item}
                )

        # 下一页url
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = "http://zu.wuhan.fang.com" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self,response):
        item = response.meta["item"]

        # 价格和房子配套设施
        item["price"] = response.xpath("//div[@class='tr-line clearfix zf_new_title']/div[1]//text()").extract()
        item["config"] = response.xpath("//div[@class='tr-line clearfix zf_new_title']/div[2]/span/text()").extract()

        # 出租方式、朝向
        modes = response.xpath("//div[@class='tr-line clearfix']/div[1]/div[@class='tt']/text()").extract()
        if modes:
            item["mode"] = modes[0]
            item["orientation"] = modes[1]

        # 户型、楼层
        house_types = response.xpath("//div[@class='tr-line clearfix']/div[2]/div[@class='tt']/text()").extract()
        if house_types:
            item["house_type"] = house_types[0]
            item["floor"] = house_types[1]

        # 面积、装修方式
        areas = response.xpath("//div[@class='tr-line clearfix']/div[3]/div[@class='tt']/text()").extract()
        if areas:
            item["area"] = areas[0]
            item["decoration_mode"] = areas[1]

        #　小区、地址
        item["community"] = response.xpath("//div[@class='tab-cont-right']/div[5]//div[1]/div[@class='rcont']/a[1]/text()").extract_first()
        item["site"] = response.xpath("//div[@class='tab-cont-right']/div[5]//div[3]/div[@class='rcont']/a[1]/text()").extract_first()
        # 房源图片
        li_list = response.xpath("//ul[@class='litImg']/li")
        item["house_img"] = []
        for li in li_list:
            img = li.xpath("./img/@src").extract_first()
            item["house_img"].append(img)

        # 房屋描述
        item["house_describe"] = response.xpath("//ul[@class='fyms_modify']/li[1]/div[2]/text()").extract_first()

        # pprint.pprint(item)
        yield item

































































