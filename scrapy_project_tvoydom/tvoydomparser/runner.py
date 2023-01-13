from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from tvoydomparser import settings
from tvoydomparser.spiders.tvoydom import TvoydomSpider



if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(TvoydomSpider)
    process.start()