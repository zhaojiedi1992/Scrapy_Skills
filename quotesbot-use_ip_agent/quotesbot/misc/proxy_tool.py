import execjs
import re
import requests
from bs4 import BeautifulSoup

class proxy_tool(object):
    def __init__(self):
        self.url = "http://www.kuaidaili.com/proxylist/1/"
        self.header = {
            "Host": "www.kuaidaili.com",
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        self.cookie=None
        self.timeout=30
        self.proxy_list=[]
    def executejs(self):
        # 提取其中的JS加密函数
        js_string = ''.join(re.findall(r'(function .*?)</script>',self.first_html))
        # 提取其中执行JS函数的参数
        js_func_arg = re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', self.first_html)[0]
        js_func_name = re.findall(r'function (\w+)',js_string)[0]
        # 修改JS函数，使其返回Cookie内容
        js_string = js_string.replace('eval("qo=eval;qo(po);")', 'return po')
        func = execjs.compile(js_string)
        return func.call(js_func_name,js_func_arg)

    def parse_cookie(self):
        string = self.cookie_str.replace("document.cookie='", "")
        clearance = string.split(';')[0]
        return {clearance.split('=')[0]: clearance.split('=')[1]}

    def get_proxy_list(self):
        # 第一次访问获取动态加密的JS
        self.first_html = self.getHtml()
        # 执行JS获取Cookie
        self.cookie_str = self.executejs()
        # 将Cookie转换为字典格式
        self.cookie = self.parse_cookie()
        #print('cookies = ',cookie)
        # 带上cookies参数，再次请求
        self.second_html =self.getHtml()
        self.parse_html()

    def parse_html(self):
        soup=BeautifulSoup(self.second_html,"lxml")
        trs=soup.select("div tbody:nth-of-type(3) tr")
        for tr in trs : 
           ip= tr.select_one(u"td[data-title='IP']").string
           port= tr.select_one(u"td[data-title='PORT']").string
           scheme= tr.select_one(u"td[data-title='类型']").string
           proxy_url=scheme +"://" + ip +":" + port
           self.proxy_list.append({"ip":ip,"port":port,"scheme":scheme,"proxy_url":proxy_url})
    def getHtml(self):
        html = requests.get(url=self.url, headers=self.header, timeout=self.timeout, cookies=self.cookie).content.decode("utf-8")
        return html
    