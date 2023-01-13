# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy as scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
import hashlib
from transliterate import translit
from pymongo import MongoClient
import re


class TvoydomparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.tvoydom

    def process_item(self, item, spider):

        item['_id'] = self.process_id(item)
        item['Details'] = self.process_details(item)
        item['category'] = self.process_category(item)
        del item['photo']
        del item['name_catalog']
        del item['catalog_children_name']
        del item['catalog_children_two_name']
        collection = self.mongo_base[spider.name]
        if collection.find_one({'_id': item['_id']}):
            old_item = collection.find_one({'_id': item['_id']})
            collection.update_one(old_item, {'$set': item})
            print(f"ОБНОВЛЕН В БАЗЕ ==> {item['Name']}; id: {item['id']}")
        else:
            collection.insert_one(item)
            print(f"ЗАПИСАН В БАЗУ ==> {item['Name']}; id: {item['id']}")
        # print(f"ЗАПИСАН В БАЗУ ==> {item['Name']}")
        # line = f"КАТАЛОГ: {item['name_catalog']} ==> КАТЕГОРИЯ: {item['catalog_children_name']} ==> РЕБЕНОК ПОДКАТЕГОРИИ: {item['catalog_children_two_name']} ==> {item['Name']}; Артикул: {item['Article']}; id: {item['_id']}"
        # with open('seve_item.txt', 'a') as f:
        #     f.write(line + '\n')
        return item

    def process_details(self, item):
        details = item['Details']
        if '<div' in details:
            details_next = re.sub(r'\<[^>]*\>', ' ', details.replace('\n', ' '))
            details_end = '. '.join([str.strip() for str in details_next.split('.')[:-1]])
        elif '@media' in details:
            reg = re.compile('[^а-яА-Я ]')
            details_end = reg.sub('', details).strip()
        else:
            details_end = item['Details']
        return details_end

    def process_category(self, item):
        name_catalog = item['name_catalog']
        catalog_children_name = item['catalog_children_name']
        catalog_children_two_name = item['catalog_children_two_name']
        if catalog_children_two_name:
            catalog = f"{name_catalog}/{catalog_children_name}/{catalog_children_two_name}".replace('//', '/')
        else:
            catalog = f"{name_catalog}/{catalog_children_name}/{catalog_children_two_name}".replace('//', '/')[:-1]
        if catalog[-1] == '/':
            catalog = catalog[-1]
        return catalog

    def process_id(self, item):
        my_id = hashlib.sha1(to_bytes(item['Name'])).hexdigest()
        return my_id


class SavePhotonPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photo']:
            list_link_fotos = [f"{item['photo']['path']}"]
            for link_foto in item['Image']:
                list_link_fotos.append(link_foto['path'])
            try:
                for link in list_link_fotos:
                    img = f"https://tvoydom.ru{link}"
                    yield scrapy.Request(img)
            except Exception as e:
                print(f"Возникла ошибка при работе метода get_media_requests с позицией: {item['name']}:- {e}")

    def item_completed(self, results, item, info):
        item['Image'] = [f"path: {itm[1]['path']}" for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        product = translit(item['Name'], language_code='ru', reversed=True)
        name_catalog = translit(item['name_catalog'], language_code='ru', reversed=True)
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{name_catalog}/{product}/{image_guid}.jpg"

        
