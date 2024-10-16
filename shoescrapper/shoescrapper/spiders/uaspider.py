import scrapy
from shoescrapper.items import ShoescrapperItem
from scrapy.loader import ItemLoader


class UarmourSpider(scrapy.Spider):
    name = 'armour'
    start_urls = ['https://www.underarmour.ca/en-ca/c/mens/shoes/']

    def parse(self, response):       
        base_url = 'https://www.underarmour.ca'
        
        for products in response.css('div.false.ProductTile_product-tile-container__flx2K.module__primary-img.false.ProductTile_split-view-disabled__3P8wI'):
            il = ItemLoader(item = ShoescrapperItem(), selector= products)

            il.add_css('name', 'a.ProductTile_product-item-link__tSc19')
            il.add_css('price', 'span.bfx-price.bfx-list-price')
            
            relative_url = products.css('a.ProductTile_product-item-link__tSc19::attr(href)').get()
            
            if relative_url:    
                il.add_value('link', base_url + relative_url)

            yield il.load_item()
            
        

        next_page = base_url + response.css('a.link_underline').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)