import scrapy
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from leroymerlenparser.items import LeroymerlenparserItem



class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/content/elbrus/moscow/ru/catalogue.navigation.json']

    def parse(self, response: HtmlResponse):
        full_catalogue_json = response.json()

        for i in range(len(full_catalogue_json.get('children'))):
            name_category_catalogue = full_catalogue_json.get('children')[i].get('name')
            for j in range(len(full_catalogue_json.get('children')[i].get('children'))):
                name_category_catalogue_child = full_catalogue_json.get('children')[i].get('children')[j].get('name')
                link_category_catalogue_child = full_catalogue_json.get('children')[i].get('children')[j].get('navigationChunk')

                yield response.follow(url=f"https://leroymerlin.ru/{link_category_catalogue_child}",
                                      callback=self.parse_category_child_two,
                                      cb_kwargs={'name_category_catalogue': name_category_catalogue,
                                                 'name_category_catalogue_child': name_category_catalogue_child})

    def parse_category_child_two(self, response: HtmlResponse, name_category_catalogue, name_category_catalogue_child):

        category_child_two = response.json()
        for i in range(len(category_child_two.get('children'))):

            name_category_child_two = category_child_two.get('children')[i].get('name')
            link_category_child_two = category_child_two.get('children')[i].get('sitePath')

            yield response.follow(url=f"https://leroymerlin.ru/{link_category_child_two}",
                                  callback=self.pars_products_cart_link,
                                  cb_kwargs={'name_category_catalogue': name_category_catalogue,
                                             'name_category_catalogue_child': name_category_catalogue_child,
                                             'name_category_child_two': name_category_child_two})

    def pars_products_cart_link(self, response: HtmlResponse, name_category_catalogue, name_category_catalogue_child, name_category_child_two):

        soup = BeautifulSoup(response.text, 'html.parser')
        next_pages = soup.find_all('a', class_='bex6mjh_plp s15wh9uj_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp')
        if next_pages:
            next_page = next_pages[0].get('href')
            yield response.follow(url=f"https://leroymerlin.ru/{next_page}",
                                  callback=self.pars_products_cart_link,
                                  cb_kwargs={'name_category_catalogue': name_category_catalogue,
                                             'name_category_catalogue_child': name_category_catalogue_child,
                                             'name_category_child_two': name_category_child_two})

        cart_links = soup.find_all('a', class_='bex6mjh_plp b1f5t594_plp p5y548z_plp pblwt5z_plp nf842wf_plp')
        for link in cart_links:
            link_product = link.get('href')
            yield response.follow(url=f"https://leroymerlin.ru/{link_product}",
                                  callback=self.pars_products,
                                  cb_kwargs={'name_category_catalogue': name_category_catalogue,
                                             'name_category_catalogue_child': name_category_catalogue_child,
                                             'name_category_child_two': name_category_child_two})


    def pars_products(self, response: HtmlResponse, name_category_catalogue, name_category_catalogue_child, name_category_child_two):

        soup = BeautifulSoup(response.text, 'html.parser')
        link_product = response.url
        specification_bs_key_product = soup.find_all('dt', class_='p14mjh7o_pdp')
        specification_bs_value_product = soup.find_all('dd', class_='pw1rm00_pdp')
        name = soup.find('h1').text
        variant_name = 'NULL'
        vendor = ''  # Бренд
        type = ''
        article = soup.find('span', class_='t12nw7s2_pdp').text  # Артикул или id продукта
        tags = 'NULL'
        description = 'NULL'
        if soup.find_all('p', class_='p11satbv_pdp'):
            details = soup.find('section-content-vlimited', class_='ppoj845_pdp').contents[0]
        else:
            details = ''
        image = soup.find_all('img', class_='p12qs89y_pdp')  # Изображение
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
        prod_type = 24
        param = 'NULL'
        param_completed = 0
        strana_proizvoditelya = ''
        obem = 'NULL'
        ves = 'NULL'
        cena_optovaya = soup.find('span', {'slot': 'price'}).text  # ЦЕНУ ПИШЕМ СЮДА!
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
        category = soup.find_all('div', class_='j6gl7k0e_s_pdp')

        yield LeroymerlenparserItem(link_product=link_product,
                                    specification_bs_key_product=specification_bs_key_product,
                                    specification_bs_value_product=specification_bs_value_product,
                                    name_category_catalogue=name_category_catalogue,
                                    name_category_catalogue_child=name_category_catalogue_child,
                                    name_category_child_two=name_category_child_two,

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