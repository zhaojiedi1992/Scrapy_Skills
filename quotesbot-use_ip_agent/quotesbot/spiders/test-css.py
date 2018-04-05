# -*- coding: utf-8 -*-
import scrapy

from twisted.internet.error import ConnectionRefusedError

class TestXCSS(scrapy.Spider):
    name = 'test-css'
    start_urls = [
        'http://www.cnblogs.com/zhaojiedi1992/',
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield  scrapy.Request(url,dont_filter=True,callback=self.parse,errback=self.parse_error)
    def parse_error(self,failure):
        self.logger.debug("="*20)
        self.logger.debug(repr(failure))
        self.logger.debug("=" * 20)
        self.logger.debug(type(failure))
        self.logger.debug("=" * 20)
        if failure.check(ConnectionRefusedError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)


    def parse(self, response):
        self.logger.debug("=" * 30)
        self.logger.debug(str(response.request.headers))
        self.logger.debug(str(response.request.meta))
        self.logger.debug("=" * 30)
        yield {"url":response.url,"proxy":response.request.meta["proxy"]}
        next_page_urls = response.css('a::attr(href)').extract()
        for next_page_url in next_page_urls:
            yield response.follow(next_page_url,dont_filter=True,callback=self.parse,errback=self.parse_error)
            
