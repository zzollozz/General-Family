# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy as scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
import hashlib
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
from transliterate import translit
import re
import json



class SportmasterParserPipeline:

    def __init__(self):
        MONGO_HOST = '178.76.234.182'
        MONGO_USER = "mr"
        MONGO_PASS = "262722Ma"

        server = SSHTunnelForwarder(
            MONGO_HOST,
            ssh_username=MONGO_USER,
            ssh_password=MONGO_PASS,
            remote_bind_address=('localhost', 27017)
        )
        server.start()
        client = MongoClient('localhost', server.local_bind_port)
        # client = MongoClient('localhost', 27017)
        self.mongo_base = client.sporymaster

    def process_item(self, item, spider):
        item['_id'] = self.process_id(item)
        item['Size'] = self.process_sizes(item)
        item['Specification'] = self.process_characteristic_product(item)
        item['Vendor'] = self.process_vendor(item)
        item['category'] = self.process_category(item)
        item['Cena_Optovaya'] = self.process_price(item)
        del item['characteristic_keys_product']
        del item['characteristic_values_product']
        del item['soup_for_sizes']
        del item['catalog_name_vid']
        del item['catalog_name']
        del item['link_product']

        collection = self.mongo_base[spider.name]
        if collection.find_one({'_id': item['_id']}):
            old_item = collection.find_one({'_id': item['_id']})
            collection.update_one(old_item, {'$set': item})
            print(f"ОБНОВЛЕН В БАЗЕ ==> {item['Name']}; id: {item['_id']}")
        else:
            collection.insert_one(item)
            print(f"ЗАПИСАН В БАЗУ ==> {item['Name']}; id: {item['_id']}")
        return item

    def process_id(self, item):
        my_id = hashlib.sha1(to_bytes(item['Name'] + item['link_product'])).hexdigest()
        return my_id

    def process_characteristic_product(self, item):
        characteristic_keys_product = item['characteristic_keys_product']
        characteristic_values_product = item['characteristic_values_product']
        characteristic_product = [f'{characteristic_keys_product[i]}: {characteristic_values_product[i]}' for i in
                                  range(len(characteristic_keys_product))]
        return characteristic_product

    def process_vendor(self, item):
        if not item['Vendor']:
            if 'Бренд' in item['characteristic_keys_product']:
                vendor = item['characteristic_values_product'][item['characteristic_keys_product'].index('Бренд')]
            else:
                vendor = item['Vendor']
        else:
            vendor = item['Vendor']
        return vendor

    def process_sizes(self, item):
        soup_for_sizes = item['soup_for_sizes']
        block_sizes = [soup_for_sizes[i] for i in range(len(soup_for_sizes)) if re.search('window.__INITIAL_STATE__', soup_for_sizes[i].text)]
        data = re.search(r'"sizes":\[(.*?)\]', block_sizes[0].text).group(1)
        deta_next = data.replace('}},', '}}oooo')
        list_data = deta_next.split('oooo')
        sizes = []
        for el in list_data:
            el_json = json.loads(el)
            if el_json['isAvailableOnline']:
                sizes.append(el_json['size'])
        return sizes

    def process_category(self, item):
        category = list(map(str.strip, item['category']))
        catalog = f'{category[-2]}/{category[-1]}'
        return catalog

    def process_price(self, item):
        price = int(item['Cena_Optovaya'].replace(u'\xa0', u'').replace('₽', ''))
        return price


class SavePhotoPipeline(ImagesPipeline):
    """ Обработка фото """
    def get_media_requests(self, item, info):
        """ Загрузка IMG """
        if item['Image']:
            try:
                for img in item['Image']:
                    yield scrapy.Request(img)
            except Exception as e:
                print(f"Возникла ошибка при работе метода get_media_requests с позицией: {item['Name']}:- {e}")

    def item_completed(self, results, item, info):
        """Формирование ссылок на фото для зранения в базе """
        item['Image'] = [f"path: {itm[1]['path']}" for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        """Создание стуктуры хранения скачаных IMG"""
        name_catalog = translit(item['catalog_name'], language_code='ru', reversed=True)
        product_vid = translit(item['catalog_name_vid'], language_code='ru', reversed=True)
        product = translit(item['Name'], language_code='ru', reversed=True)
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()

        return f"{name_catalog}/{product_vid}/{product}/{image_guid}.jpg"

