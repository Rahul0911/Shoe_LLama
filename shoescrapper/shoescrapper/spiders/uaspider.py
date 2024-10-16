import scrapy


class UarmourSpider(scrapy.Spider):
    name = 'armour'
    start_urls = ['https://www.underarmour.ca/en-ca/c/mens/shoes/']

    def parse(self, response):
        
        base_url = "https://www.underarmour.ca"
        
        for products in response.css('div.false.ProductTile_product-tile-container__flx2K.module__primary-img.false.ProductTile_split-view-disabled__3P8wI'):
            yield {
                'name': products.css('a.ProductTile_product-item-link__tSc19::text').get(),
                'price': products.css('span.bfx-price.bfx-list-price::text').get().replace('$', ''),
                'link': base_url + products.css('a.ProductTile_product-item-link__tSc19').attrib['href'],
            }

        next_page = base_url + response.css('a.link_underline').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)