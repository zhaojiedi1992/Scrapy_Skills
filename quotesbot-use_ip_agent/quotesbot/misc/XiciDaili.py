from .ip_proxy_tool import ip_proxy_tool,ip_info
from bs4 import BeautifulSoup
import logging
logger=logging.getLogger(__name__)

class XiciDaili(ip_proxy_tool):
    def __init__(self):
        super(XiciDaili,self).__init__()
        self.url="http://www.xicidaili.com/nn/1"

    def parse_proxy_list(self):
        soup=BeautifulSoup(self.html,"lxml")
        trs=soup.select("#ip_list tr")
        for tr in trs[1:] :
            ip= tr.select_one("td:nth-of-type(2)").string
            port= tr.select_one("td:nth-of-type(3)").string
            scheme= tr.select_one(u"td:nth-of-type(6)").string
            alive_time=tr.select_one("td:nth-of-type(9)").string
            verify_time=tr.select_one("td:nth-of-type(10)").string
            proxy_url=scheme.lower() +"://" + ip +":" + port

            info=ip_info(ip,port,scheme,alive_time,verify_time,proxy_url)
            if ip is None or port is None or scheme is None or alive_time is None or verify_time is None or proxy_url is None:
                continue
            if self.is_valid_proxy(info):
                self.proxy_list.append(info)


             