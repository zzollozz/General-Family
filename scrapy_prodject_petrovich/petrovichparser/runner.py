from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from petrovichparser import settings
from petrovichparser.spiders.petrovichru import PetrovichruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(PetrovichruSpider)
    process.start()
