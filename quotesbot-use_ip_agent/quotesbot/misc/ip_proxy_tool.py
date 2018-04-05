import requests
import random 
import operator
import logging
from pprint import pprint
logger=logging.getLogger(__name__)

class ip_info():
    def __init__(self,ip,port,scheme,alive_time,verify_time,proxy_url):
        #ip，port ,协议类型，存活时间，最新的验证时间，scheme://ip:port作为代理地址，当前是否有效
        self.ip=ip
        self.port=port
        self.scheme=scheme
        self.alive_time=alive_time
        self.verify_time=verify_time
        self.proxy_url=proxy_url
        self.current_valid=True

    def __repr__(self):
        return str(self.__dict__)

class ip_proxy_tool(object):
    def __init__(self):
        self.proxy_list=[]
        self.proxy_list_black=[]
        self.url = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.cookie=None
        self.timeout=30
        self.encoding='utf-8'
        #self.fetch_method="random"
        #self.fetch_method="alive_time"
        #self.fetch_method="online_time"
        #self.fetch_method="verify_time"
        self.fetch_method="first"
        self.current_proxy=None

        self.test_url="https://www.baidu.com/"
        self.need_to_valid=True

    def parse_proxy_list():
        pass
    def fresh(self):
        self.get_html()
        self.parse_proxy_list()
    def move_to_black_list(self,one):
        if isinstance(one,ip_info):
            one.current_valid=False
            self.proxy_list.remove(one)
            self.proxy_list_black.append(one)
        else:
            tmp=[ i for i in self.proxy_list if i.proxy_url == one]
            if len(tmp) >0:
                self.proxy_list.remove(tmp[0])
                self.proxy_list_black.append(tmp[0])

    def fetch_one_proxy_from_list(self):
        if self.current_proxy is not None and self.current_proxy.current_valid:
            return self.current_proxy
        if len(self.proxy_list)==0:
            self.fresh()
        if self.fetch_method =="first" :
            one=self.proxy_list[0]
            self.move_to_black_list(one)
            self.current_proxy=one
            return
        if self.fetch_method=="random" or self.fetch_method is None:
            one= random.choice(self.proxy_list)
            self.move_to_black_list(one)
            self.current_proxy=one
            return
        if self.fetch_method =="alive_time" or self.fetch_method=="verify_time" :
            cmpfun = operator.attrgetter(self.fetch_method) 
            self.proxy_list.sort(key = cmpfun,reverse=True)
            one=self.proxy_list[0]
            self.move_to_black_list(one)
            self.current_proxy=one
            return

             
    def get_html(self):
        self.html = requests.get(url=self.url, headers=self.header, timeout=self.timeout, cookies=self.cookie).content.decode(self.encoding)
    def is_valid_proxy(self,one):
        if self.need_to_valid is False:
            return True
        
        test_header={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        proxy={one.scheme:one.ip +":" + str(one.port)}
        status_code=requests.get(url=self.test_url, headers=test_header,proxies=proxy).status_code
        if status_code == 200: 
            return True
        return False

