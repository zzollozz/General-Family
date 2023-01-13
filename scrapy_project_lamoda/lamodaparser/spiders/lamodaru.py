import scrapy


class LamodaruSpider(scrapy.Spider):
    name = 'lamodaru'
    allowed_domains = ['lamoda.ru']
    urls = 'http://www.lamoda.ru'
    # start_urls = ['https://www.lamoda.ru/_blocks/menu/?genders=women&json=1',
    #               'https://www.lamoda.ru/_blocks/menu/?genders=men&json=1',
    #               'https://www.lamoda.ru/_blocks/menu/?genders=children&json=1']
    start_urls = ['https://www.lamoda.ru/_blocks/menu/?genders=women&json=1']

    def parse(self, response):
        data = response.json()
        block_menu = data.get('payload').get('seo').get('canonical')
        block_media = data.get('settings').get('media_cdn')
        id_category = data.get('header').get('menu_gender')
        category = data.get('header').get('menu_flexible').get('category')
        pod_category = {}
        print()
        for i in category:
            pod_category_name = i.get('title').get('text')
            pod_category_link = i.get('title').get('url')
            if pod_category_name in 'Одежда, Обувь, Аксессуары, Спорт':
                pod_category[pod_category_name] = f'{self.urls}{pod_category_link}'
        print()