# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GtjSpider(CrawlSpider):
    name = 'gtj'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        i['url'] = response.url
        i['proxy']=response.meta["proxy"]
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
