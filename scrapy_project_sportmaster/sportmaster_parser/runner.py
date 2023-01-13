from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from sportmaster_parser import settings
from sportmaster_parser.spiders.sportmaster import SportmasterSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SportmasterSpider)
    process.start()

# scrapy crawl sportmaster
