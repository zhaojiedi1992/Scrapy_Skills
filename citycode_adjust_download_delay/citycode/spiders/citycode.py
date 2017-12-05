# -*- coding: utf-8 -*-
import scrapy


class CityCodeSpiderXPath(scrapy.Spider):
    name = 'citycode'
    start_urls = [
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html',
    ]

    def parse(self, response):
        for pro in response.css('.provincetr a'):
            yield {
                'text': pro.css('::text').extract_first(),
                'sub_herf': response.urljoin(pro.css('::attr(href)').extract_first()), 
            }
