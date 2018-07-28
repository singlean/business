# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from business.settings import USER_AGENT_LIST
import random
from fake_useragent import UserAgent

class RandomUserAgent(object):

    user_agent = UserAgent()

    def process_request(self, request, spider):

        # UA = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = self.user_agent.chrome































