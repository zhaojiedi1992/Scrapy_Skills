# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item


class QuotesbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class MoviePFItem(scrapy.Item):
    m_id=scrapy.Field()#
    u_id=scrapy.Field()
    pf=scrapy.Field()
    name=scrapy.Field()
    lx=scrapy.Field()#类型
    dq=scrapy.Field()#地区
    dbpf=scrapy.Field()#评分
    phlink=scrapy.Field()#电影图链接
    sytime=scrapy.Field()#上瘾时间
    pianchang=scrapy.Field()#片长
    summary=scrapy.Field()#内容
    dy=scrapy.Field()
    bj=scrapy.Field()
    zy=scrapy.Field()
    proxy=scrapy.Field()

class DoubanmoiveItem(scrapy.Item):
    name=Field()#电影名
    year=Field()#上映年份
    score=Field()#豆瓣分数
    director=Field()#导演
    classification=Field()#分类
    actor=Field()#演员


class ScrapycnblogsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    refer_url=scrapy.Field()
    url= scrapy.Field()
    edit_url=scrapy.Field()
    title=scrapy.Field()
    #content=scrapy.Field()
    post_id=scrapy.Field()
    view_count=scrapy.Field()
    comment_count=scrapy.Field()