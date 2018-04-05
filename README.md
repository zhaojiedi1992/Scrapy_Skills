# Scrapy_Skills
使用Scrapy抓取页面的一些被ban的技巧使用

## scrapy官方提供的几种防止被ban的方法
参考地址： [https://doc.scrapy.org/en/latest/topics/practices.html#avoiding-getting-banned](https://doc.scrapy.org/en/latest/topics/practices.html#avoiding-getting-banned)

主要有如下几条

1.  设置一个list集合存放userAgent,每次请求从集合里面选一个userAgent
2.  禁用cookies,有些网址启用cookies来识别bot.
3.  使用下载延迟download_delay，有些网址对单位时间内请求次数有限制，过多请求会被禁的。
4.  如果可能的话使用谷歌缓存，而不是直接请求网址。
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

### 调整下载延迟 citycode_adjust_download_delay

我们默认启动爬虫，下载延迟DOWNLOAD_DELAY=0,是没有延迟的，这样会给抓取的网址造成巨大压力。 有些网址在防火墙级别或者web服务器级别可能会有限制。 
所以我们如果对我们的抓取速度要求不高的话。 尽量调高下载延迟值的设定
```python
DOWNLOAD_DELAY=2
```
其实不仅仅使用DOWNLOAD_DELAY,我们还是可以调整这个参数相关的其他参数，比如如下几个参数
```python
AUTOTHROTTLE_ENABLED :是否启动自适应下载延迟，默认是False
AUTOTHROTTLE_START_DELAY:自适应下载延迟调整的起始值，默认是5，单位为s
AUTOTHROTTLE_MAX_DELAY：自适应下载延迟调整的最大值，默认是60，单位s
AUTOTHROTTLE_TARGET_CONCURRENCY:自适应算法计算的最佳值。
AUTOTHROTTLE_DEBUG：是否启用自适应debug功能
CONCURRENT_REQUESTS_PER_DOMAIN：每个域的并发请求数量，默认是不限制的
CONCURRENT_REQUESTS_PER_IP：每个ip的并发请求数量，默认是不限制的。
DOWNLOAD_DELAY：下载延迟，
```
这几个参数的设置。我这里不详细说了。 具体的传送门如下： [https://doc.scrapy.org/en/latest/topics/autothrottle.html](https://doc.scrapy.org/en/latest/topics/autothrottle.html)

### googlecache
这个我暂时没法尝试， 百度没有cache这个好像。 等以后在做这个案例

### 使用ip池 
proxymesssh github地址： https://github.com/mizhgun/scrapy-proxymesh
```cmd
pip install scrapy-proxymesh -i https://pypi.tuna.tsinghua.edu.cn/simple
```
