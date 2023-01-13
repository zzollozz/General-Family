import scrapy
from scrapy.http import HtmlResponse
from petrovichparser.items import PetrovichparserItem


class PetrovichruSpider(scrapy.Spider):
    name = 'petrovichru'
    allowed_domains = ['petrovich.ru']
    url_catalog = 'https://moscow.petrovich.ru/catalog/'
    # start_urls = ['https://api.petrovich.ru/catalog/v2.2/sections/tree/3?city_code=msk&client_id=pet_site']
    start_urls = ['https://api.petrovich.ru/catalog/v2.3/sections/tree/3?city_code=msk&client_id=pet_site']
    limit = 50

    def parse(self, response: HtmlResponse):
        data = response.json()
        for catalog in data.get('data').get('sections'):                    # Все категории 7 штук
            for catalog_child in catalog.get('sections'):                   # дети Первой Категории 10 шт
                if catalog_child.get('sections'):
                    for page_products in catalog_child.get('sections'):      # Внуки Первой Категории
                        product_qty = page_products.get('product_qty')
                        next_page = 0
                        if product_qty >= self.limit:
                            while next_page <= product_qty:
                                link_catalogs = f"https://api.petrovich.ru/catalog/v2.2/sections/{page_products.get('code')}?offset={next_page}&limit={self.limit}&sort=popularity_desc&city_code=msk&client_id=pet_site"
                                yield response.follow(url=link_catalogs,
                                                      callback=self.parse_products_links)
                                next_page += self.limit
                        else:
                            link_catalogs = f"https://api.petrovich.ru/catalog/v2.2/sections/{page_products.get('code')}?offset={next_page}&limit={self.limit}&sort=popularity_desc&city_code=msk&client_id=pet_site"
                            yield response.follow(url=link_catalogs,
                                                  callback=self.parse_products_links)

                            if page_products.get('sections'):  # Если есть то следующее вложение
                                for page_product_child in page_products.get('sections'):
                                    product_qty = page_product_child.get('product_qty')
                                    next_page = 0
                                    if product_qty > self.limit:
                                        while next_page <= product_qty:
                                            link_catalogs = f"https://api.petrovich.ru/catalog/v2.2/sections/{page_product_child.get('code')}?offset={next_page}&limit={self.limit}&sort=popularity_desc&city_code=msk&client_id=pet_site"
                                            yield response.follow(url=link_catalogs,
                                                                  callback=self.parse_cart_product)
                                            next_page += self.limit
                                    else:
                                        link_catalogs = f"https://api.petrovich.ru/catalog/v2.2/sections/{page_products.get('code')}?offset={next_page}&limit={self.limit}&sort=popularity_desc&city_code=msk&client_id=pet_site"
                                        yield response.follow(url=link_catalogs,
                                                              callback=self.parse_products_links)


    def parse_products_links(self, response: HtmlResponse):
        data_products = response.json()
        for product in data_products.get('data').get('products'):
            linc_product = f"https://api.petrovich.ru/catalog/v2.2/products/{product.get('code')}?city_code=msk&client_id=pet_site"
            yield response.follow(url=linc_product,
                                  callback=self.parse_cart_product)


    def parse_cart_product(self, response):
        link_api_product = response.url
        data_product = response.json()
        link_product = f"https://moscow.petrovich.ru/catalog/{data_product.get('data').get('product').get('section').get('code')}/{data_product.get('data').get('product').get('code')}/"
        name = data_product.get('data').get('product').get('title')
        variant_name = 'NULL'
        vendor = ''  # Бренд
        type = ''
        article = data_product.get('data').get('product').get('code')  # Артикул или id продукта
        tags = 'NULL'
        description = data_product.get('data').get('product').get('description_no_html').get('description')     # Краткое описание
        details = data_product.get('data').get('product').get('extended_description')  # Детальное описание
        image = data_product.get('data').get('product').get('images')  # Изображение
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
        specification = data_product.get('data').get('product').get('properties')   # характеристики
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
        prod_type = 26
        param = 'NULL'
        param_completed = 0
        strana_proizvoditelya = ''  # Страна производителя
        obem = 'NULL'
        ves = 'NULL'
        cena_optovaya = data_product.get('data').get('product').get('price').get('retail')  # ЦЕНУ ПИШЕМ СЮДА!
        min_partiya = ''
        nds = 0
        bar_code = data_product.get('data').get('product').get('barcode')
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
        category = data_product.get('data').get('product').get('breadcrumbs')

        yield PetrovichparserItem(
            link_api_product=link_api_product,
            link_product=link_product,

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
            ncSMO_Image=nc_smo_image,
            category=category
            )
