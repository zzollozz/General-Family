from shutil import which
# Scrapy settings for tvoydomparser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tvoydomparser'

SPIDER_MODULES = ['tvoydomparser.spiders']
NEWSPIDER_MODULE = 'tvoydomparser.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'INFO'
# LOG_FILE = 'log_tvoydom.txt'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tvoydomparser (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'

IMAGES_STORE = 'photos'
# IMAGES_STORE = '/Users/dzonsmitt/Desktop/Work_Program/General_Family/scrapy_project_tvoydom/tvoydomparser/photos'


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
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tvoydomparser.middlewares.TvoydomparserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'tvoydomparser.middlewares.TvoydomparserDownloaderMiddleware': 543,
   # 'tvoydomparser.middlewares.SeleniumMiddleware': 800,
}

# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('/Users/dzonsmitt/Desktop/Work_Program/General_Family/scrapy_project_tvoydom/chromedriver')
# SELENIUM_DRIVER_ARGUMENTS = ['--start-maximized', '--no-sandbox']  # '--headless' if using chrome instead of firefox

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'tvoydomparser.pipelines.TvoydomparserPipeline': 300,
   # 'tvoydomparser.pipelines.SavePhotonPipeline': 200,
   # 'tvoydomparser.pipelines.CSVPipeline': 400,
   # 'tvoydomparser.pipelines.MysqlPipelineTwo': 400,
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

# MYSQL_HOST = '192.168.1.77'
# MYSQL_DBNAME = 'test_my_db'
# MYSQL_USER = 'bob'
# MYSQL_PASSWORD = '111(qwe$-BOB'
# MYSQL_CHARSET = 'utf8mb4'
# MYSQL_PORT = 3306
