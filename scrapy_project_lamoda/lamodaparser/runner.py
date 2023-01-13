from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lamodaparser import settings
from lamodaparser.spiders.lamodaru import LamodaruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LamodaruSpider)
    process.start()

