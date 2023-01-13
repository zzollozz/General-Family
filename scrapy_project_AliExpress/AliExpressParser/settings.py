# Scrapy settings for AliExpressParser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AliExpressParser'

SPIDER_MODULES = ['AliExpressParser.spiders']
NEWSPIDER_MODULE = 'AliExpressParser.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'    #  DEBUG    ERROR  INFO
# LOG_FILE = 'log_AliExpressParser.txt


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'auchanparser (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'

IMAGES_STORE = 'photos'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://aliexpress.ru/?spm=a2g0o.tm800006433.1000001.1.579e7bdan2I8YJ',
    'Origin': 'https://aliexpress.ru',
    'DNT': '1',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    'Cookie': 'aer_abid=b9c443bdd59685c9; xman_us_f=x_locale=ru_RU&x_l=0&x_c_chg=1&acs_rt=504753ad34d74080bca7e487bd60ef8f; acs_usuc_t=x_csrf=1axqc227tiq79&acs_rt=d34c350a81c7462fb25b1c5a3a09526f; xman_t=r2iPe05aQsrVdB9odtZxlkoFP9pPP1FsLuiojjBgOuVJlwb+Mi/3cLiVzRT9JcXD; xman_f=IrppzI7kHhVJ6VYR8/1P5D4h8oRkMePZM83a7HbNxhkAXwIt9vQFCMGutX5v34aApYfoJnBWZ8YQExfw+mMWUqRblzJHJ4xQr4lK/YCls3mKiBsfsz1UPQ==; intl_locale=ru_RU; aep_usuc_f=site=rus&c_tp=RUB&region=RU&b_locale=ru_RU; intl_common_forever=UfHHibHc/S4AgDGburm8mfxRrlOFeTPy/lk2mM+w4SMm/DMGqVcyIw==; JSESSIONID=910E2402782ED1B9A5FAD5D2BACEF942; cna=vQpDG7rfr2YCAbA7MCFfa0kv; isg=BAQE91cPOkut746H0iiWTIKx1oT2HSiHQb_Gex6lk0-SSaQTRizXFt3riXmRymDf; l=eBgiZrh7Llxzc5etBOfalurza779IIOYYuPzaNbMiOCP_w165WjNB6bds-YBCn6Nh6Q2R3JrX9ODBeYBcnvnRwzA69je1CHmn; tfstk=cIRVBN2Sg1xS8Q1dis1Zlg2gnB7AZ6AH6u71nDydprJ3CNXlicEOrbPdU9azjtf..; xlly_s=1; aer_ab=82',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # 'Content-Length': '0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'AliExpressParser.middlewares.AliexpressparserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'AliExpressParser.middlewares.AliexpressparserDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'AliExpressParser.pipelines.AliexpressparserPipeline': 300,
   'AliExpressParser.pipelines.SavePhotoPipeline': 200,
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
