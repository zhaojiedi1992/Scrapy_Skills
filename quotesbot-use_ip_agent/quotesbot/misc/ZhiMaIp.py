from .ip_proxy_tool import ip_proxy_tool,ip_info
import json
import logging
logger=logging.getLogger(__name__)

class ZhiMaIp(ip_proxy_tool):
    def __init__(self):
        super(ZhiMaIp,self).__init__()
        self.url="http://webapi.http.zhimacangku.com/getip?num=10&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions="

    def parse_proxy_list(self):
        objs=json.loads(self.html)
        if objs["code"] ==0:
            for obj in objs["data"]:
                ip= obj["ip"]
                port= obj["port"]
                scheme= "http"
                alive_time=None
                verify_time=None
                proxy_url=scheme.lower() +"://" + ip +":" + str(port)
                info=ip_info(ip,port,scheme,alive_time,verify_time,proxy_url)
                if self.is_valid_proxy(info):
                    self.proxy_list.append(info)


             