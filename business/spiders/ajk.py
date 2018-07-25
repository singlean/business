# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider


class AjkSpider(RedisSpider):
    name = 'ajk'
    allowed_domains = ['anjuke.com']
    # start_urls = ['https://wh.zu.anjuke.com/?from=navigation']
    redis_key = "ajk"

    def parse(self, response):

        # 房源列表
        div_list = response.xpath("//div[@class='list-content']/div[@class='zu-itemmod  ']")
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./div[@class='zu-info']/h3/a/text()").extract_first()
            item["url"] = div.xpath("./div[@class='zu-info']/h3/a/@href").extract_first()

            if item["url"]:

                yield scrapy.Request(
                    url=item["url"],
                    callback=self.parse_detail,
                    meta={"item":item}
                )

        # 下一页url
        next_url = response.xpath("//a[@class='aNxt']/@href").extract_first()
        if next_url:
            print(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )


    def parse_detail(self,response):
        item = response.meta["item"]

        # 租金
        price = response.xpath("//ul[@class='house-info-zufang cf']/li[1]/span[1]//text()").extract()
        if price:
            item["price"] = price[0].strip() + price[1].strip()
        # 付款方式
        item["payment_method"] = response.xpath("//ul[@class='house-info-zufang cf']/li[1]/span[2]/text()").extract_first()

        # 户型、面积、朝向、楼层、装修方式
        item["house_type"] = response.xpath("//ul[@class='house-info-zufang cf']/li[2]/span[2]/text()").extract_first()
        item["house_area"] = response.xpath("//ul[@class='house-info-zufang cf']/li[3]/span[2]/text()").extract_first()
        item["orientation"] = response.xpath("//ul[@class='house-info-zufang cf']/li[4]/span[2]/text()").extract_first()
        item["floor"] = response.xpath("//ul[@class='house-info-zufang cf']/li[5]/span[2]/text()").extract_first()
        item["decoration_method"] = response.xpath("//ul[@class='house-info-zufang cf']/li[6]/span[2]/text()").extract_first()
        item["type_info"] = response.xpath("//ul[@class='house-info-zufang cf']/li[7]/span[2]/text()").extract_first()
        item["community_site"] = response.xpath("//ul[@class='house-info-zufang cf']/li[8]/a/text()").extract()

        # 租用方式,房源图片
        item["rent_method"] = response.xpath("//li[@class='title-label-item rent']/text()").extract_first()
        item["house_img"] = response.xpath("//div[@id='surround_pic_wrap']/div[@class='img_wrap']/img/@data-src").extract()

        yield item






































