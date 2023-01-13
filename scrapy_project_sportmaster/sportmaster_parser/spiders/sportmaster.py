import scrapy
from scrapy.http import HtmlResponse
from sportmaster_parser.items import SportmasterParserItem
from bs4 import BeautifulSoup


class SportmasterSpider(scrapy.Spider):
    name = 'sportmaster'
    allowed_domains = ['sportmaster.ru']
    start_urls = ['http://www.sportmaster.ru']

    def parse(self, response: HtmlResponse):
        list_link_categorys = [i for n, i in enumerate(
            response.selector.xpath("//li[contains(@data-selenium,'section-gender')]//a/@href").getall()) if i not in
                               response.selector.xpath("//li[contains(@data-selenium,'section-gender')]//a/@href").getall()[:n]]

        for link in list_link_categorys:
            yield response.follow(url=f'https://www.sportmaster.ru{link}',
                                  callback=self.get_catalog_parse)

    def get_catalog_parse(self, response: HtmlResponse):
        catalog_name = response.selector.xpath("//h1/text()").get().strip()
        catalog_category = response.selector.xpath("//a[@class='sm-link sm-link_black DmFZd']/@href").getall()
        if catalog_category:
            if catalog_name == 'Женская одежда' or catalog_name == 'Мужская одежда'\
                    or catalog_name == 'Одежда для мальчиков' or catalog_name == 'Одежда для девочек':
                catalog_category.remove(catalog_category[-1])


        for link in catalog_category:
            yield response.follow(url=f'https://www.sportmaster.ru{link}',
                                  callback=self.get_category_parse,
                                  cb_kwargs={'catalog_name': catalog_name})

    def get_category_parse(self, response: HtmlResponse, catalog_name):
        next_page = response.selector.xpath("//a[@class='sm-pagination__next sm-link sm-link_black']/@href").get()
        if next_page:
            yield response.follow(url=f'https://www.sportmaster.ru{next_page}',
                                  callback=self.get_catalog_parse)

        catalog_name_vid = response.selector.xpath("//div[@class='sm-catalog app-content']//li[2]//text()").get().strip()
        link = response.selector.xpath("//div[@class='sm-product-card sm-product-grid__product has-hover']//a/@href").getall()
        link_products = [i for n, i in enumerate(link) if i not in link[:n]]
        for link in link_products:
            yield response.follow(url=f'https://www.sportmaster.ru{link}',
                                  callback=self.product_parse,
                                  cb_kwargs={'catalog_name': catalog_name,
                                             'catalog_name_vid': catalog_name_vid})

    def product_parse(self, response: HtmlResponse, catalog_name, catalog_name_vid):
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_for_sizes = soup.find_all('script')

        link_product = response.url
        characteristic_keys_product = response.selector.xpath(
            "//div[@class='sm-product-properties__table-wrp']//span/text()").getall()
        characteristic_values_product = response.selector.xpath(
            "//div[@class='sm-product-properties__table-wrp']//span/pre/text()").getall()

        name = response.selector.xpath("//h1/text()").get().strip()     # Наименование
        variant_name = 'NULL'
        if not response.selector.xpath("//span[@class='sm-text brand_name sm-text-text-16 sm-text-medium']/text()").get():
            vendor = ''
        else:
            vendor = response.selector.xpath("//span[@class='sm-text brand_name sm-text-text-16 sm-text-medium']/text()").get().strip()  # Бренд
        type = ''
        article = response.selector.xpath("//span[@class='sm-product-sku-code__codes']/text()").get()  # Артикул или id продукта
        tags = 'NULL'
        description = 'NULL'
        details = response.selector.xpath("//span[@class='sm-text sm-text-text-14 sm-text-regular zGy_D']//text()").getall()  # Краткое описание
        image = response.selector.xpath("//div[@class='swiper-wrapper']//img/@data-src").getall()  # Изображение
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
        prod_type = 23
        param = 'NULL'
        param_completed = 0
        strana_proizvoditelya = ''
        obem = 'NULL'
        ves = 'NULL'
        cena_optovaya = response.selector.xpath("//span[@class='sm-amount price__catalog sm-amount_default']//span/text()").get()  # ЦЕНУ ПИШЕМ СЮДА!
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
        category = response.selector.xpath("//span[@class='sm-text item__text sm-text-text-12 sm-text-regular']/text()").getall()

        yield SportmasterParserItem(soup_for_sizes=soup_for_sizes,
                                    link_product=link_product,
                                    catalog_name=catalog_name,
                                    catalog_name_vid=catalog_name_vid,
                                    characteristic_keys_product=characteristic_keys_product,
                                    characteristic_values_product=characteristic_values_product,

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

