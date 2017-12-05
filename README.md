# Scrapy_Skills
使用Scrapy抓取页面的一些被ban的技巧使用

## scrapy官方提供的几种防止被ban的方法
参考地址： [https://doc.scrapy.org/en/latest/topics/practices.html#avoiding-getting-banned](https://doc.scrapy.org/en/latest/topics/practices.html#avoiding-getting-banned)

主要有如下几条

1.  设置一个list集合存放userAgent,每次请求从集合里面选一个userAgent
2.  禁用cookies,有些网址启用cookies来识别bot.
3.  使用下载延迟download_delay，有些网址对单位时间内请求次数有限制，过多请求会被禁的。
4.  如果肯能的话使用谷歌缓存，而不是直接请求网址。
5.  使用ip池，比如ProxyMesh，scrapoxy
6.  使用高度分布的下载器，比如Crawlera


### useragent的使用案例 quotesbot-use_user_agent
这个项目是使用了一个CustomUserAgentMiddleware自定义的中间件，给每个请求头添加User-Agent信息。 核心代码如下：
```python
from .agents import AGENTS,AGENTS_ALL
import random

class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS_ALL)
        request.headers['User-Agent'] = agent
```
这个就是设定一个用户代理中间件，给每个请求头信息， 这个用户代理是从一个list中随机取出来的。

再设置中我们需要禁用默认的用户代理，启用我们的代理
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'quotesbot.misc.middleware.CustomUserAgentMiddleware': 543,
}
```
这里我们在终端测试的时候，打印日志我让打印到指定的文件中去了。
```python
from datetime import datetime
LOG_FILE=datetime.now().strftime("%Y%m%d%H%M%S") + '_scrapy.log'
```
我们在爬虫中打印下我们的请求头信息。确保我们的请求使用了代理。也就是个验证把。
```python
        self.logger.info("*" * 40 + "request.headers" + "*" * 40)
        self.logger.info(str(response.request.headers))
```

### 禁用cookie的使用案例 quotesbot-cookie_disabled

这个没啥说的。 就是在settings中修改
```python
COOKIES_ENABLED=False
```
有些网站是根据cookie识别出身份的， 如果我们禁用cookie，就无法识别我们的身份了。 

