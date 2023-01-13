from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from auchanparser import settings
from auchanparser.spiders.auchanru import AuchanruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AuchanruSpider)
    process.start()
