# -*- coding: utf-8 -*-
import scrapy

from twisted.internet.error import ConnectionRefusedError

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield  scrapy.Request(url,dont_filter=True,callback=self.parse,errback=self.parse_error)
    def parse_error(self,failure):
        self.logger.error("="*20)
        self.logger.error(repr(failure))
        self.logger.error("=" * 20)
        self.logger.error(type(failure))
        self.logger.error("=" * 20)
        if failure.check(ConnectionRefusedError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)


    def parse(self, response):
        self.logger.error("=" * 30)
        self.logger.debug(str(response.request.headers))
        #self.logger.debug(str(response.request["meta"]))
        self.logger.error("=" * 30)
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

