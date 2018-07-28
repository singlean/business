# -*- coding: utf-8 -*-
import scrapy,re
from scrapy_redis.spiders import RedisSpider


class XljiaSpider(RedisSpider):
    name = 'xljia'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://wh.lianjia.com/zufang/pg1/']
    redis_key = "xljia"

    def parse(self, response):

        # 区级分类列表
        a_list = response.xpath("//div[@id='filter-options']/dl[1]//a")[1:]
        for a in a_list:
            item = {}
            item["district_href"] = a.xpath("./@href").extract_first()
            item["district_name"] = a.xpath("./text()").extract_first()

            if item["district_href"]:
                item["district_href"] = "https://wh.lianjia.com" + item["district_href"]

                yield scrapy.Request(
                    url=item["district_href"],
                    callback=self.parse_one_list,
                    meta={"item":item},
                    dont_filter=True
                )

    def parse_one_list(self,response):
        item = response.meta["item"]

        # 街道列表
        a_list = response.xpath("//div[@class='option-list sub-option-list']/a")[1:]

        for a in a_list:
            item["street_href"] = a.xpath("./@href").extract_first()
            item["street_name"] = a.xpath("./text()").extract_first()

            if item["street_href"]:
                item["street_href"] = "https://wh.lianjia.com" + item["street_href"]

                yield scrapy.Request(
                    url=item["street_href"],
                    callback=self.parse_two_list,
                    meta={"item":item},
                    dont_filter=True
                )

    def parse_two_list(self,response):
        item = response.meta["item"]
        # 房源列表
        li_list = response.xpath("//ul[@class='house-lst']/li")
        for li in li_list:
            item["title"] = li.xpath("./div[@class='info-panel']/h2/a/text()").extract_first()
            item["url"] = li.xpath("./div[@class='info-panel']/h2/a/@href").extract_first()

            if item["url"]:
                yield scrapy.Request(
                    url=item["url"],
                    callback=self.parse_detail,
                    meta={"item":item}
                )

        # 下一页地址
        page = response.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract_first()
        total,current = re.findall(r'\{"totalPage":(\d+?),"curPage":(\d+?)\}',page)[0]

        if int(current) < int(total):
            if "pg" not in response.url:
                next_url = response.url + "pg{}/".format(int(current)+1)
            else:
                next_url = response.url.split("pg")[0] + "pg{}/".format(int(current)+1)

            print(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_two_list,
                meta={"item":item}
        )

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




























