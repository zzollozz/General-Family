# Scrapy settings for petrovichparser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'petrovichparser'

SPIDER_MODULES = ['petrovichparser.spiders']
NEWSPIDER_MODULE = 'petrovichparser.spiders'
LOG_ENABLED = True
LOG_LEVEL = 'INFO'    #  DEBUG    ERROR  INFO
LOG_FILE = 'log_petrovich.txt'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'auchanparser (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'

IMAGES_STORE = 'photos'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Content-Type':	'application/json; charset=UTF-8',
    'Cookie': 'qrator_msid=1657746657.586.5D6IMPLvtcRUKNjZ-gmfnqsp1o60f5qomkgbpma4ldtqeb58h; SNK=117; u__typeDevice=desktop; SIK=dQAAAL-5ywSERu0RM6sKAA; SIV=1; C_NCTxBR8IKDEpzLekU0NO-ahucoA=AAAAAAAACEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8D8AAICQrLzpQV2-8jR9ofGGVoy9bHAzTJY; _gcl_au=1.1.487108749.1657746784; _ga_XW7S332S1N=GS1.1.1657746784.1.1.1657746892.0; _ga=GA1.1.734478558.1657746784; ssaid=95f213f0-02f0-11ed-920a-ad4bfa13f215; dd__lastEventTimestamp=1657746784976; dd__persistedKeys=[%22custom.lastViewedProductImages%22]; dd_custom.lastViewedProductImages=[]; __tld__=null; rrpvid=446103541257331; rcuid=62cf3561fa505eac5dbb70aa; mindboxDeviceUUID=33e00772-8924-453e-b695-601bef4ff3ce; directCrm-session=%7B%22deviceGuid%22%3A%2233e00772-8924-453e-b695-601bef4ff3ce%22%7D'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'petrovichparser.middlewares.PetrovichparserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'petrovichparser.middlewares.PetrovichparserDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'petrovichparser.pipelines.PetrovichparserPipeline': 300,
   'petrovichparser.pipelines.SavePhotoPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
