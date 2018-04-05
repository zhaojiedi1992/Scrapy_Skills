from .ip_proxy_tool import ip_proxy_tool,ip_info
import json
import logging
logger=logging.getLogger(__name__)

class JingDongWanXiang(ip_proxy_tool):
    def __init__(self):
        super(JingDongWanXiang,self).__init__()
        self.url="https://way.jd.com/jisuapi/proxy?num=10&area=&areaex=&port=8080,80&portex=3306&protocol=1,2&type=1&appkey=b198438a2f0dbdce9721760bd49866d0"
        self.need_to_valid=False

    def parse_proxy_list(self):
        objs=json.loads(self.html)
        for obj in objs["result"]["result"]["list"]:
            ip= obj["ip"].split(":")[0]
            port=obj["ip"].split(":")[1]
            scheme= obj["protocol"].lower()
            alive_time=None
            verify_time=None
            proxy_url=scheme.lower() +"://" + ip +":" + str(port)
            info=ip_info(ip,port,scheme,alive_time,verify_time,proxy_url)
            if self.is_valid_proxy(info):
                self.proxy_list.append(info)


             