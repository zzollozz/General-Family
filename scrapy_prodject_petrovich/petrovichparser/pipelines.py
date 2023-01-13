# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import scrapy as scrapy
import hashlib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
from transliterate import translit
import re

class PetrovichparserPipeline:
    def __init__(self):
        # MONGO_HOST = '89.108.123.78' # 89.108.123.78   178.76.234.182
        # MONGO_USER = "root"
        # MONGO_PASS = "cL2rW6oP7hoB9z"
        #
        # server = SSHTunnelForwarder(
        #     MONGO_HOST,
        #     ssh_username=MONGO_USER,
        #     ssh_password=MONGO_PASS,
        #     remote_bind_address=('localhost', 27017)
        # )
        # server.start()
        # client = MongoClient('localhost', server.local_bind_port)
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.petrovich

    def process_item(self, item, spider):
        item['_id'] = self.process_id(item)
        item['Description'] = self.process_description(item)
        item['Details'] = self.process_details(item)
        item['Specification'] = self.process_specification(item)
        item['Vendor'] = self.process_vendor(item)
        item['Type'] = self.process_type(item)
        item['category'] = self.process_category(item)

        del item['link_api_product']
        del item['link_product']

        collection = self.mongo_base[spider.name]

        if not collection.find_one({'_id': item['_id']}):
            count = collection.count_documents({})
            item['elem_id'] = count + 1
            collection.insert_one(item)
            print(f"ЗАПИСАН В БАЗУ ==> {item['Name']}; elem_id: {item['elem_id']}")
        # else:
        #     old_item = collection.find_one({'_id': item['_id']})
        #     item['elem_id'] = old_item['elem_id']
        #     collection.update_one(old_item, {'$set': item})
        #     print(f"ОБНОВЛЕН В БАЗЕ ==> {item['Name']}; elem_id: {item['elem_id']}")
        return item

    def process_id(self, item):
        my_id = hashlib.sha1(to_bytes(item['Name'] + item['link_product'])).hexdigest()
        return my_id

    def process_description(self, item):
        description = re.sub("^\s+|\n|\t|\tB|\xa0|\r|\s+$", '', item['Description'])
        return description

    def process_details(self, item):
        if item['Details']:
            res = re.sub(r'(\<(/?[^>]+)>)', '', item['Details'])
            result = re.sub("^\s+|\n|\t|\tB|\xa0|\r|\s+$", '', res)
            return result

    def process_specification(self, item):
        specification = {item['Specification'][i].get('title'): item['Specification'][i].get('value')[0].get('title') for i in range(len(item['Specification']))}
        return specification

    def process_vendor(self, item):
        vendor = item['Specification'].get('Бренд')
        return vendor

    def process_type(self, item):
        return item['Specification'].get('Тип товара')


    def process_category(self, item):
        category = [el.get('title') for el in item['category']]
        if len(category) > 3:
            category = category[:3]
        return ','.join(category).replace(',', '/')


class SavePhotoPipeline(ImagesPipeline):
    """ Обработка фото """
    def get_media_requests(self, item, info):
        """ Загрузка IMG """
        images = [img for img in item['Image']]
        if images:
            try:
                for img in images:
                    yield scrapy.Request(f"http:{img}")
            except Exception as e:
                print(f"Возник Косяк со скачиванием: {item['Name']}: {item['link_product']}:==> {e}")

    def item_completed(self, results, item, info):
        """Формирование ссылок на фото для зранения в базе """
        item['Image'] = [f"path: {itm[1]['path']}" for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        """Создание стуктуры хранения скачаных IMG"""
        category = [el.get('title') for el in item['category']]
        name_category_catalogue = translit(category[0], language_code='ru', reversed=True)
        name_category_catalogue_child = translit(category[1], language_code='ru', reversed=True)
        name_category_child_two = translit('' if not len(item['category']) > 3 else category[2], language_code='ru', reversed=True)

        product = translit(item['Name'], language_code='ru', reversed=True)
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        if name_category_child_two:
            return f"{name_category_catalogue}/{name_category_catalogue_child}/{name_category_child_two}/{product}/{image_guid}.jpg"
        else:
            return f"{name_category_catalogue}/{name_category_catalogue_child}/{product}/{image_guid}.jpg"
