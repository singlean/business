# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider


class LjiaSpider(RedisSpider):
    name = 'ljia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://wh.lianjia.com/zufang/pg1/']

    def parse(self, response):
        # 房源列表
        li_list = response.xpath("//ul[@class='house-lst']/li")
        for li in li_list:
            item = {}
            item["title"] = li.xpath("./div[@class='info-panel']/h2/a/text()").extract_first()
            item["url"] = li.xpath("./div[@class='info-panel']/h2/a/@href").extract_first()

            if item["url"]:
                yield scrapy.Request(
                    url=item["url"],
                    callback=self.parse_detail,
                    meta={"item":item}
                )

        # 下一页地址
        page = dict(response.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract_first())
        total = page["totalPage"]
        current = page["curPage"]
        if current < total:
            next_url = "https://wh.lianjia.com/zufang/pg{}/".format(current+1)
            print(next_url)

            # yield scrapy.Request(
            #     url=next_url,
            #     callback=self.parse
            # )
            #



    def parse_detail(self,response):
        item = response.meta["item"]

        # 价格、面积、户型、楼层、朝向、小区、位置、时间
        item["price"] = response.xpath("//div[@class='price ']/span[1]/text()").extract_first()
        item["area"] = response.xpath("//div[@class='zf-room']/p[1]/text()").extract_first()
        item["house_type"] = response.xpath("//div[@class='zf-room']/p[2]/text()").extract_first()
        item["floor"] = response.xpath("//div[@class='zf-room']/p[3]/text()").extract_first()
        item["orientation"] = response.xpath("//div[@class='zf-room']/p[4]/text()").extract_first()
        item["community"] = response.xpath("//div[@class='zf-room']/p[6]/a[1]/text()").extract_first()
        item["site"] = response.xpath("//div[@class='zf-room']/p[7]/a/text()").extract()
        item["time"] = response.xpath("//div[@class='zf-room']/p[8]/text()").extract_first()

        # 房源设施
        config = response.xpath("//div[@class='zf-tag']/ul/li/text()").extract()
        item["config"] = [i.strip() for i in config if i.strip()]

        # 房源图片
        item["house_img"] = response.xpath("//div[@class='thumbnail']/ul/li/img/@src").extract()

        yield item





