import scrapy
import json
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from tvoydomparser.items import TvoydomparserItem
# scrapy crawl tvoydom

class TvoydomSpider(scrapy.Spider):
    name = 'tvoydom'
    allowed_domains = ['tvoydom.ru']
    start_urls = ['http://www.tvoydom.ru']

    def parse(self, response: HtmlResponse):
        soup = BeautifulSoup(response.text, "html.parser")
        block_info = soup.find('vue-catalog-popup').attrs
        menu = json.loads(block_info[':menu'])

        for catalog in menu.get('children')[:1]:
            catalog_name = catalog.get('name')

            for catalog_children in catalog.get('children')[:1]:    
                catalog_children_name = catalog_children.get('name')
                catalog_children_link = catalog_children.get('link')
                catalog_children_two_name = ''

                yield scrapy.FormRequest(f'{self.start_urls[0]}/api/internal{catalog_children_link[:-1]}',
                                         method='POST',
                                         callback=self.parse_products,
                                         formdata={'pageSize': '10000',
                                                   'sortColumn': 'popularity',
                                                   'sortDirection': 'desc'},
                                         headers={'csrf_token': '56465018e82d60c4d693eca19802fb5a'},
                                         cb_kwargs={'catalog_name': catalog_name,
                                                    'catalog_children_name': catalog_children_name,
                                                    'catalog_children_two_name': catalog_children_two_name})

                for catalog_children_two in catalog_children.get('children'):
                    catalog_children_two_name = catalog_children_two.get('name')
                    catalog_children_two_link = catalog_children_two.get('link')

                    yield scrapy.FormRequest(f'{self.start_urls[0]}/api/internal{catalog_children_two_link[:-1]}',
                                             method='POST',
                                             callback=self.parse_products,
                                             formdata={'pageSize': '10000',
                                                       'sortColumn': 'popularity',
                                                       'sortDirection': 'desc'},
                                             headers={'csrf_token': '56465018e82d60c4d693eca19802fb5a'},
                                             cb_kwargs={'catalog_name': catalog_name,
                                                        'catalog_children_name': catalog_children_name,
                                                        'catalog_children_two_name': catalog_children_two_name})


    def parse_products(self, response: HtmlResponse, catalog_name, catalog_children_name, catalog_children_two_name):
        j_data = response.json()

        for card in range(len(j_data.get('cards'))):

            photo = j_data.get('cards')[card].get('photo')

            name = j_data.get('cards')[card].get('name')  # название
            variant_name = 'NULL'
            vendor = j_data.get('cards')[card].get('brand')  # Бренд
            type = ''
            article = j_data.get('cards')[card].get('code')  # Артикул или id продукта
            tags = 'NULL'
            description = 'NULL'
            details = j_data.get('cards')[card].get('description')  # Краткое описание
            image = j_data.get('cards')[card].get('catalogPhotos')  # Изображение
            price = 0
            currency = 'RUB'
            currency_value = ''
            old_price = 'NULL'
            currency_minimum = 'RUB'
            currency_minimum_value = 'NULL'
            weight = 'NULL'
            package_size1 = 'NULL'
            package_size2 = 'NULL'
            package_size3 = 'NULL'
            units = ''
            units_value = 'NULL'
            stock_units = 100
            top_selling_multiplier = 'NULL'
            top_selling_addition = 'NULL'
            vat = 'NULL'
            sales_notes = ''
            item_id = 'NULL'
            import_source_id = 0
            rate_total = 'NULL'
            rate_count = 'NULL'
            material = 'NULL'
            size = 'NALL'
            variant_volume = 'NULL'
            for_use = 'NULL'
            indications = 'NULL'
            composition = 'NULL'
            effect = 'NULL'
            specification = j_data.get('cards')[card].get('props')  # характеристики
            tabs_qty = 'NULL'
            has_variants = 0
            no_yandex = 0
            no_google = 0
            no_mail = 0
            top_sales = ''
            action_text = 'NULL'
            action = 0
            complect = 'NULL'
            market_desc = 'NULL'
            expressd_delivery = 0
            data = ''
            data2 = ''
            prod_type = 22
            param = 'NULL'
            param_completed = 0
            strana_proizvoditelya = ''
            obem = 'NULL'
            ves = 'NULL'
            cena_optovaya = j_data.get('cards')[card].get('price')  # ЦЕНУ ПИШЕМ СЮДА!
            min_partiya = ''
            nds = 0
            bar_code = 'NULL'
            sku = 'NULL'
            vendor_code = 'NULL'
            length = 'NULL'
            width = 'NULL'
            height = 'NULL'
            color = 'NULL'
            belki = ''
            zhiry = ''
            uglevody = ''
            fruktoza = ''
            saxaroza = ''
            energeticheskaya_cennost = ''
            srok_godnosti_dnej = ''
            inner_id = 0
            identifier_exists = 'true'
            pitatelnaya_cennost = ''
            vitaminy_i_mineraly = ''
            usloviya_xraneniya = ''
            min_order_qty = 1
            on_sklad = 100
            main_good = 0
            similar_product_ids = 'NULL'
            keyword = 0
            nc_title = 'NULL'
            nc_keywords = 'NULL'
            nc_description = 'NULL'
            nc_smo_title = 'NULL'
            nc_smo_description = 'NULL'
            nc_smo_image = 'NULL'

            yield TvoydomparserItem(photo=photo,
                                    name_catalog=catalog_name,
                                    catalog_children_name=catalog_children_name,
                                    catalog_children_two_name=catalog_children_two_name,
                                    Name=name,
                                    VariantName=variant_name,
                                    Vendor=vendor,
                                    Type=type,
                                    Article=article,
                                    Tags=tags,
                                    Description=description,
                                    Details=details,
                                    Image=image,
                                    Price=price,
                                    Currency=currency,
                                    Currency_Value=currency_value,
                                    OldPrice=old_price,
                                    CurrencyMinimum=currency_minimum,
                                    CurrencyMinimum_Value=currency_minimum_value,
                                    Weight=weight,
                                    PackageSize1=package_size1,
                                    PackageSize2=package_size2,
                                    PackageSize3=package_size3,
                                    Units=units,
                                    Units_Value=units_value,
                                    StockUnits=stock_units,
                                    TopSellingMultiplier=top_selling_multiplier,
                                    TopSellingAddition=top_selling_addition,
                                    VAT=vat,
                                    SalesNotes=sales_notes,
                                    ItemID=item_id,
                                    ImportSourceID=import_source_id,
                                    RateTotal=rate_total,
                                    RateCount=rate_count,
                                    Material=material,
                                    Size=size,
                                    Variant_Volume=variant_volume,
                                    ForUse=for_use,
                                    Indications=indications,
                                    Composition=composition,
                                    Effect=effect,
                                    Specification=specification,
                                    TabsQty=tabs_qty,
                                    HasVariants=has_variants,
                                    NoYandex=no_yandex,
                                    NoGoogle=no_google,
                                    NoMail=no_mail,
                                    TopSales=top_sales,
                                    ActionText=action_text,
                                    Action=action,
                                    Complect=complect,
                                    MarketDesc=market_desc,
                                    ExpressDelivery=expressd_delivery,
                                    Data=data,
                                    Data2=data2,
                                    ProdType=prod_type,
                                    Param=param,
                                    ParamCompleted=param_completed,
                                    Strana_proizvoditelya=strana_proizvoditelya,
                                    Obem=obem,
                                    Ves=ves,
                                    Cena_Optovaya=cena_optovaya,
                                    Min_partiya=min_partiya,
                                    NDS=nds,
                                    BarCode=bar_code,
                                    SKU=sku,
                                    VendorCode=vendor_code,
                                    Length=length,
                                    Width=width,
                                    Height=height,
                                    Color=color,
                                    Belki=belki,
                                    ZHiry=zhiry,
                                    Uglevody=uglevody,
                                    Fruktoza=fruktoza,
                                    Saxaroza=saxaroza,
                                    Energeticheskaya_cennost=energeticheskaya_cennost,
                                    Srok_godnosti_dnej=srok_godnosti_dnej,
                                    InnerID=inner_id,
                                    IdentifierExists=identifier_exists,
                                    Pitatelnaya_cennost=pitatelnaya_cennost,
                                    Vitaminy_i_mineraly=vitaminy_i_mineraly,
                                    Usloviya_xraneniya=usloviya_xraneniya,
                                    MinOrderQty=min_order_qty,
                                    On_Sklad=on_sklad,
                                    MainGood=main_good,
                                    SimilarProductIds=similar_product_ids,
                                    Keyword=keyword,
                                    ncTitle=nc_title,
                                    ncKeywords=nc_keywords,
                                    ncDescription=nc_description,
                                    ncSMO_Title=nc_smo_title,
                                    ncSMO_Description=nc_smo_description,
                                    ncSMO_Image=nc_smo_image
                                    )

