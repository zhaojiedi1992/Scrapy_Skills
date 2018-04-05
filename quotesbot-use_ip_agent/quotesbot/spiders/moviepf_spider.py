import scrapy
from ..items import MoviePFItem
from scrapy import Request

class MovieSpider(scrapy.Spider):
    name='moviepf'

    #cookie1='bid=BHoR6ID6iZ4; ll="108296"; __yadk_uid=jfvQxP5RvsyQLe5UbsQgTPTsoIsTfYzT; gr_user_id=ca89b08f-d5fe-4901-a034-5476e752176e; viewed="1105583_5257905_21622482"; ct=y; _vwo_uuid_v2=2F6F1F4C58BA2B74297D802A908F03EC|67b71ce0767385c0adbad71482bdbb9d; ps=y; _ga=GA1.2.951420023.1512358879; ap=1; __utmv=30149280.16990; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1513168819%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D9KwMRPWnkaouEC7FhIDy7Un8eXIusDZF_WDBxRRaQya%26wd%3D%26eqid%3Dfc31513100008f05000000045a311fb0%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.951420023.1512358879.1513038826.1513168821.25; __utmc=30149280; __utmz=30149280.1513168821.25.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt_douban=1; __utmt=1; _pk_id.100001.8cb4=a18c7dd9cf3e08f4.1490779400.27.1513170087.1513007842.; __utmb=30149280.39.10.1513168821; _gid=GA1.2.989486334.1513170098; _gat_UA-7019765-1=1; dbcl2="169902938:OjvjZiYyOYA"'
    start_urls = [
        'https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=60',
    ]
    headers = {
        #'cookie':cookie1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    #print('22222222222')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers,dont_filter=True)


    def parse(self,response):
        self.logger.info(response.status)
        yield {"url":response.url,"proxy":response.meta["proxy"]}

        links=response.css("a::attr(href)").extract()
        self.logger.info(str(links))
        for link in links:
           yield  response.follow(link,dont_filter=True)









