import logging 
import urllib.request
from bs4 import BeautifulSoup
import threading
from .proxy_tool import proxy_tool
#from .XiciDaili import  XiciDaili
# from .JingDongWanXiang import JingDongWanXiang
from .ZhiMaIp import ZhiMaIp
from pprint import  pprint , PrettyPrinter
from twisted.internet.error import ConnectionLost,ConnectionRefusedError

logger=logging.getLogger(__name__)


class CustomHttpProxyMiddleware(object):
    proxy_url_list=[]
    lock=threading.Lock()
    proxy_tool=ZhiMaIp()

    def __init__(self):
        logger.info(self.__class__.__name__+"初始化工作开始...")
        if len(self.__class__.proxy_tool.proxy_list) == 0:
            if self.__class__.lock.acquire():
                if len(self.__class__.proxy_tool.proxy_list) == 0 :
                    self.__class__.proxy_tool.fresh()
                    logger.info(str(self.__class__.proxy_tool.proxy_list))
                self.__class__.lock.release()
        logger.info(self.__class__.__name__+"初始化工作完成...")

    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.can_use_proxy(request):
            #proxy_url=random.choice(self.__class__.proxy_url_list)["proxy_url"]
            #proxy_url=self.__class__.proxy_url_list[0]["proxy_url"]
            self.__class__.proxy_tool.fetch_one_proxy_from_list()
            logger.info("请求前的url" + self.__class__.proxy_tool.current_proxy.proxy_url)
            try:
                request.meta['proxy'] = self.__class__.proxy_tool.current_proxy.proxy_url
            except Exception as e:
                logging.critical("Exception %s" % e)
    def process_response(self ,request, response, spider):
        
        if response.status == 403:
            logger.info("process_response抓到403")
            self.__class__.proxy_tool.move_to_black_list(request.meta["proxy"])
            #self.__class__.proxy_tool.fresh()
            self.__class__.proxy_tool.fetch_one_proxy_from_list()
            meta=request.meta
            meta["proxy"]=self.__class__.proxy_tool.current_proxy.proxy_url
            return  request.replace(meta=meta,dont_filter=True)
        return response
    # def process_exception(self,request, exception, spider):
    #     logger.info("抓取到一个异常在process_exception"+str(exception)+str(type(exception)))
    #     if isinstance(exception,(ConnectionLost,ConnectionRefusedError)):
    #         self.__class__.proxy_tool.fetch_one_proxy_from_list()
    #         meta=request.meta
    #         meta["proxy"]=self.__class__.proxy_tool.current_proxy.proxy_url
    #         return  request.replace(meta=meta,dont_filter=True)
    def can_use_proxy(self, request):
        """
        如果能使用请求，返回True,否则返回False,
        你可以在这里对request的属性进行判断，比如说request.meta["depth"]
        """
        return True

                
