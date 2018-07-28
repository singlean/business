# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class MNPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "mn":
            with open("./mn.txt","a+") as f:
                print(item)
                f.write(str(item))
                f.write("\n")
        return item


class KFDLPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "kfdl":
            with open("./kfdl.txt","a+") as f:
                f.write(str(item))
                f.write("\n")
                print("保存成功")
        return item


class FTXPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["ftx"]

    def process_item(self, item, spider):
        if spider.name == "ftx":
            self.collection.insert(item)
            print("保存成功")

        return item


class LJIAPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["ljia"]

    def process_item(self, item, spider):
        if spider.name == "ljia":
            self.collection.insert(item)
            print("保存成功")
            # print(item)
        return item


class AJKAPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["ajk"]

    def process_item(self, item, spider):
        if spider.name == "ajk":
            self.collection.insert(item)
            print("保存成功")
            # print(item)
        return item


class XLJIAPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["xljia"]

    def process_item(self, item, spider):
        if spider.name == "xljia":
            self.collection.insert(item)
            print("保存成功")
            # print(item)
        return item
























