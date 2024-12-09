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
                il.add_value('link', response.urljoin(relative_url))

            yield il.load_item()
            
        next_page = response.css('a[data-testid="pager-next"]::attr(href)').get()

        if next_page:
            next_page_url = response.urljoin(next_page)
            self.log(f"Next page URL: {next_page_url}")  # Add this line to log the next page URL
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.log("No next page found.")  # Log if no next page is found