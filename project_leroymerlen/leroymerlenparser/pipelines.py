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




class LeroymerlenparserPipeline:
    # def __init__(self):
        # MONGO_HOST = '192.168.1.77'
        # MONGO_USER = "mr"
        # MONGO_PASS = "262722Ma"
        #
        # server = SSHTunnelForwarder(
        #     MONGO_HOST,
        #     ssh_username=MONGO_USER,
        #     ssh_password=MONGO_PASS,
        #     remote_bind_address=('localhost', 27017)
        # )
        # server.start()
        # client = MongoClient('localhost', server.local_bind_port)
        # client = MongoClient('localhost', 27017)
        # self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        item['_id'] = self.process_id(item)
        item['Article'] = self.process_article(item)
        item['Cena_Optovaya'] = self.process_cena_optovaya(item)
        item['Specification'] = self.process_specification(item)
        item['Vendor'] = self.process_vendor(item)
        item['category'] = self.process_category(item)
        item['Details'] = self.process_details(item)
        del item['specification_bs_key_product']
        del item['specification_bs_value_product']
        del item['name_category_catalogue']
        del item['name_category_catalogue_child']
        del item['name_category_child_two']
        del item['link_product']
        print(f"ТОВАР В БАЗУ ЗАПИСАН ==> {item['Name']}")
        # collection = self.mongo_base[spider.name]
        # if collection.find_one({'_id': item['_id']}):
        #     old_item = collection.find_one({'_id': item['_id']})
        #     item['elem_id'] = old_item['elem_id']
        #     collection.update_one(old_item, {'$set': item})
        #     print(f"ОБНОВЛЕН В БАЗЕ ==> {item['Name']}; elem_id: {item['elem_id']}")
        # else:
        #     count = collection.count_documents({})
        #     item['elem_id'] = count + 1
        #     collection.insert_one(item)
        #     print(f"ЗАПИСАН В БАЗУ ==> {item['Name']}; elem_id: {item['elem_id']}")
        return item

    def process_id(self, item):
        my_id = hashlib.sha1(to_bytes(item['Name'] + item['link_product'])).hexdigest()
        return my_id

    def process_article(self, item):
        article = item['Article'].replace('Арт.', '').strip()
        return article

    def process_cena_optovaya(self, item):
        return int(item['Cena_Optovaya'].replace('\xa0', ''))

    def process_specification(self, item):
        specification_bs_key_product = [key.text for key in item['specification_bs_key_product']]
        specification_bs_value_product = [value.text for value in item['specification_bs_value_product']]
        specification = dict(zip(specification_bs_key_product, specification_bs_value_product))
        return specification

    def process_vendor(self, item):
        if 'Марка' in item['Specification']:
            vendor = item['Specification']['Марка']
        else:
            vendor = ''
        return vendor

    def process_details(self, item):
        if item['Details']:
            try:
                details = [(details_el.text).replace('\n', ' ') for item_el in item['Details'] for details_el in
                           item_el.contents]
                for i in range(len(details) - 1):
                    if 'скачать инструкцию' in details[i].lower():
                        details = details[i + 1:]
                        break
                details = ' '.join(details)
            except AttributeError as ae:
                print(f"Косяк ==> {ae} ==> {item['Name']}: {item['link_product']}")
                res = [re.sub(r'(\<(/?[^>]+)>)', '', el.text) for el in item['Details']]
                ress = [el.replace('\n', ' ') for el in res if el]
                details = ' '.join(ress)
        else:
            details = ''
        return details

    def process_category(self, item):
        list_catalog = [el.text for el in item['category'][0]]
        if len(list_catalog) > 2:
            catalog = f"{list_catalog[-3]}/{list_catalog[-2]}/{list_catalog[-1]}"
        else:
            catalog = f"{item['name_category_catalogue']}/{item['name_category_catalogue_child']}"
        return catalog


class SavePhotoPipeline(ImagesPipeline):
    """ Обработка фото """
    def get_media_requests(self, item, info):
        """ Загрузка IMG """
        images = [img.get('src') for img in item['Image']]
        if images:
            try:
                for img in images:
                    yield scrapy.Request(img)
            except Exception as e:
                print(f"Возникла ошибка при работе метода get_media_requests с позицией: {item['Name']}:- {e}")

    def item_completed(self, results, item, info):
        """Формирование ссылок на фото для зранения в базе """
        item['Image'] = [f"path: {itm[1]['path']}" for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        """Создание стуктуры хранения скачаных IMG"""
        name_category_catalogue = translit(item['name_category_catalogue'], language_code='ru', reversed=True)
        name_category_catalogue_child = translit(item['name_category_catalogue_child'], language_code='ru', reversed=True)
        name_category_child_two = translit(item['name_category_child_two'], language_code='ru', reversed=True)
        product = translit(item['Name'], language_code='ru', reversed=True)
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{name_category_catalogue}/{name_category_catalogue_child}/{name_category_child_two}/{product}/{image_guid}.jpg"


        
