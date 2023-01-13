import scrapy
from scrapy.http import HtmlResponse
from AliExpressParser.items import AliexpressparserItem
import json
import re


class AliexpressruSpider(scrapy.Spider):
    name = 'aliexpressru'
    allowed_domains = ['aliexpress.ru']
    # start_urls = ['http://aliexpress.ru/']
    start_urls = ['https://aliexpress.ru/aer-api/v1/bx/categories/1']
    number_page = 0


    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            yield scrapy.FormRequest(url,
                                     method='POST',
                                     callback=self.parse,
                                     )

    def parse(self, response: HtmlResponse):
        j_categories = response.json()
        for category in j_categories['categories']:
            category_for_path = category.get('name')
            name_category = category.get('title')[0].get('text')
            for column in category.get('columns'):
                for group_column in column:
                    group_name = group_column.get('groupTitle')
                    if re.search('https:', group_column.get('groupUrl')):
                        group_link = group_column.get('groupUrl')
                    else:
                        group_link = f"https:{group_column.get('groupUrl')}"
                    yield response.follow(group_link,
                                          callback=self.parse_pages_products)
                                          # cb_kwargs={'group_name': group_name})

                    if group_column.get('items'):
                        for item in group_column.get('items'):
                            item_name = item.get('name')
                            if re.search('https:', item.get('url')):
                                item_url = item.get('url')
                            else:
                                item_url = f"https:{item.get('url')}"
                            if item_url != group_link:
                                yield response.follow(item_url,
                                                      callback=self.parse_pages_products)
                                                      # cb_kwargs={'item_name': item_name})

    def parse_pages_products(self, response: HtmlResponse):

        flag_pages = response.xpath("//span[@class='ali-kit_Base__base__104pa1 ali-kit_Base__default__104pa1 ali-kit_Label__label__1n9sab ali-kit_Label__size-s__1n9sab SearchPagination_SearchPagination__label__wjhu3']").getall()
        if flag_pages:
            if len(response.url.split('?')) > 1:
                if response.url.split('?')[1].split('=')[0] == 'page':
                    next_page = f"{response.url.split('?')[0]}?page={int(response.url.split('?')[1].split('=')[1]) + 1}"
                else:
                    next_page = f"{response.url.split('?')[0]}?page=1"
            else:
                next_page = f"{response.url}?page=1"
            # print(f'страница yield parse_pages_products ==> {next_page}')
            yield response.follow(next_page,
                                  callback=self.parse_pages_products)

        product_cards = response.xpath("//a[@class='product-snippet_ProductSnippet__galleryBlock__tusfnx']/@href").getall()
        catalogs = response.xpath("//div[@class='SearchBreadcrumbs_SearchBreadcrumbs__breadcrumbsContainer__b61od']//text()").getall()
        for product in product_cards:
            # print(f'страница product из product_cards ==> https://aliexpress.ru{product}')
            yield response.follow(f"https://aliexpress.ru{product}",
                                  callback=self.parse_product_cards,
                                  cb_kwargs={'catalogs': catalogs})



    def parse_product_cards(self, response: HtmlResponse, catalogs):
        link_product = response.url
        setting_colors = response.xpath("//img[@class='ali-kit_Image__image__1jaqdj Product_SkuValueGalleryItem__img__1alsi']/@src").getall()
        param_item = response.xpath("//div[@class='Product_Info__container__1v6uf']//text()").getall()

        name = response.xpath("//h1[@class='ali-kit_Base__base__104pa1 ali-kit_Base__default__104pa1 ali-kit_Heading__heading__1mk5o0 ali-kit_Heading__size-xxl__1mk5o0 Product_Name__productTitleText__hntp3']/text()").get()
        variant_name = 'NULL'
        vendor = ''  # Бренд
        type = ''
        article = ''  # Артикул или id продукта
        tags = 'NULL'
        description = ''  # Краткое описание
        details = ''  # Детальное описание
        image = response.xpath("//div[@class='Product_GalleryBarItem__barItem__11qng']//@src").getall()  # Изображение
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
        size = response.xpath("//div[@class='Product_SkuValueButtonItem__buttonItem__341wr']/span/text()").getall()      #'NALL'
        variant_volume = 'NULL'
        for_use = 'NULL'
        indications = 'NULL'
        composition = 'NULL'
        effect = 'NULL'
        specification = response.xpath("//div[@class='Characteristics_Characteristics__wrapper__16s65']//text()").getall()  # характеристики
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
        prod_type = 28
        param = 'NULL'
        param_completed = 0
        strana_proizvoditelya = ''  # Страна производителя
        obem = 'NULL'
        ves = 'NULL'
        cena_optovaya = response.xpath("//span[@class='ali-kit_Base__base__104pa1 ali-kit_Base__default__104pa1 ali-kit_Base__strong__104pa1 price ali-kit_Price__size-xl__12ybyf Product_Price__current__1uqb8 product-price-current']//text()").get()  # ЦЕНУ ПИШЕМ СЮДА!
        min_partiya = ''
        nds = 0
        bar_code = ''
        sku = 'NULL'
        vendor_code = 'NULL'
        length = 'NULL'
        width = 'NULL'
        height = 'NULL'
        color = response.xpath("//img[@class='ali-kit_Image__image__1jaqdj Product_SkuValueGalleryItem__img__1alsi']/@alt").getall()   #'NULL'
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
        category = response.xpath("//ol[@class='BreadCrumbs_BreadCrumbs__ol__5s5mv']//text()").getall()

        yield AliexpressparserItem(
                                link_product=link_product,
                                catalogs=catalogs,

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

