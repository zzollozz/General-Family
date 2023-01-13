# Scrapy settings for auchanparser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.settings.default_settings import DEFAULT_REQUEST_HEADERS

BOT_NAME = 'auchanparser'

SPIDER_MODULES = ['auchanparser.spiders']
NEWSPIDER_MODULE = 'auchanparser.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'    #  DEBUG    ERROR  INFO
# LOG_FILE = 'log_auchan.txt'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'auchanparser (+http://www.yourdomain.com)'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0'

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
    # 'Cookie': f"qrator_jsid={'1658655551.140.T8UyEtLsIaHYxRhb-ccnu0cbdq48os34q2sffa05tgu8udvqj'}",
    'Cookie': 'rrpvid=531924397339250; mindboxDeviceUUID=7718a4d7-a8d4-4c4c-bd7a-90ab79aa8ff1; directCrm-session=%7B%22deviceGuid%22%3A%227718a4d7-a8d4-4c4c-bd7a-90ab79aa8ff1%22%7D; rcuid=62d7a7f94e5b73f396add2e2; _csrf=557e9f6f8a82b185c80194b25f2430c48d15d53fc06b55fa23c41ffb1257b672a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22lMCXyv3wnro6F7b-G74g5Nna-flqHsQY%22%3B%7D',
    # 'Cookie': 'isAddressPopupShown_=true; region_id=1; merchant_ID_=1; methodDelivery_=1; _GASHOP=001_Mitishchi; rrpvid=531924397339250; mindboxDeviceUUID=7718a4d7-a8d4-4c4c-bd7a-90ab79aa8ff1; directCrm-session=%7B%22deviceGuid%22%3A%227718a4d7-a8d4-4c4c-bd7a-90ab79aa8ff1%22%7D; rcuid=62d7a7f94e5b73f396add2e2; acceptCookies_=true; qrator_jsid=1658302450.192.sv4l9IwEqNdj6F6u-1insde52t2srqj272mfb6moli720ljtt'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'auchanparser.middlewares.AuchanparserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'auchanparser.middlewares.AuchanparserDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'auchanparser.pipelines.AuchanparserPipeline': 300,
   'auchanparser.pipelines.SavePhotoPipeline': 200,
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
# HTTPERROR_ALLOWED_CODES  = [401]
# HTTPERROR_ALLOWED_CODES  = [406]