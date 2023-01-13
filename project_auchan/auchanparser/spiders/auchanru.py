import scrapy
from scrapy.http import HtmlResponse
from auchanparser.items import AuchanparserItem


class AuchanruSpider(scrapy.Spider):
    name = 'auchanru'
    allowed_domains = ['auchan.ru']
    url = 'https://www.auchan.ru'
    start_urls = ['https://www.auchan.ru/catalog/kolbasnye-izdeliya/']


    def parse(self, response: HtmlResponse):                                                         # Сбор Общего каталога Всех категорий
        catalogs = response.xpath("//a[@class='youMayNeedCategoryItem active css-191a632']/@href").getall()
        for page_product in catalogs[:17]:
            link = f"{self.url}{page_product}"
            yield response.follow(url=link,
                                  callback=self.parse_category_cild)

    def parse_category_cild(self, response: HtmlResponse):                                          # Отправка Выбранной категории Продуктов
        category_child = response.xpath("//a[@class='linkToSubCategory active css-pmm0xw']/@href").getall()

        for link_vid_category_child in category_child:

            link = f"{self.url}{link_vid_category_child}"
            yield response.follow(url=link,
                                  callback=self.parse_products_pages)

    def parse_products_pages(self, response: HtmlResponse):                                          # Отправка Одного продукта с страници для его разбора

        products_links = response.xpath("//a[@class='linkToPDP active css-1kl2eos']/@href").getall()
        next_page = response.xpath("//li[@class='pagination-arrow pagination-arrow--right']/a/@href").get()

        if next_page:
            link = f"{self.url}{next_page}"
            yield response.follow(url=link,
                                  callback=self.parse_products_pages)

        for page_product_child in products_links:
            link = f"{self.url}{page_product_child}"
            yield response.follow(url=link,
                                  callback=self.parse_product)


    def parse_product(self, response: HtmlResponse):                                                  # Разбор продукта

        specification_key = response.xpath("//th/text()").getall()
        specification_value = response.xpath("//td/text()").getall()

        link_product = response.url
        name = response.xpath("//h1/text()").get()
        variant_name = 'NULL'
        vendor = ''  # Бренд
        type = ''
        article = ''  # Артикул или id продукта
        tags = 'NULL'
        description = ''  # Краткое описание
        details = response.xpath("//div[@class='css-ivaahx']/text()").get()  # Детальное описание
        image = response.xpath("//img[@class='picture__img']/@src").getall()  # Изображение
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
        specification = ''  # характеристики
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
        prod_type = 27
        param = 'NULL'
        param_completed = 0
        strana_proizvoditelya = ''  # Страна производителя
        obem = 'NULL'
        ves = 'NULL'
        cena_optovaya = response.xpath("//div[@class='fullPricePDP css-1129a1l']/text()").get()  # ЦЕНУ ПИШЕМ СЮДА!
        min_partiya = ''
        nds = 0
        bar_code = ''
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
        category = response.xpath("//span[@itemprop='name']/text()").getall()

        yield AuchanparserItem(
            link_product=link_product,
            specification_key=specification_key,
            specification_value=specification_value,
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