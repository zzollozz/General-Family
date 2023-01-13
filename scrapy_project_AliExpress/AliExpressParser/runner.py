from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from AliExpressParser import settings
from AliExpressParser.spiders.aliexpressru import AliexpressruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AliexpressruSpider)
    process.start()