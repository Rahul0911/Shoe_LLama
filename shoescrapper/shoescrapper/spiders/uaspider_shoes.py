import scrapy

class uacrawl(scrapy.Spider):
    name = 'armour_2'
    start_urls = ['https://www.underarmour.ca/en-ca/c/girls/shoes/']

    def parse(self, response):
        for link in response.css('div.false.ProductTile_product-tile-container__flx2K.module__primary-img.false.ProductTile_split-view-disabled__3P8wI a::attr(href)'):
            url = response.urljoin(link.get())
            yield response.follow(url, callback = self.parse_deep, meta={'product_url': url})

        next_page = response.css('a[data-testid="pager-next"]::attr(href)').get()

        if next_page:
            next_page_url = response.urljoin(next_page)
            self.log(f"Next page URL: {next_page_url}")  # Add this line to log the next page URL
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.log("No next page found.")  # Log if no next page is found

    def parse_deep(self, response):
        product_url = response.meta['product_url']
        about = response.css('p.ProductIntro_whats-it-do__l6gyJ::text').get()
        product_dna = ','.join(response.css('div[data-testid="accordion-content"] li::text').getall())
        
        yield {
            'name': response.css('h1.VariantDetailsEnhancedProductName_productNameWording__3RZXk::text').get(),
            'price': response.css('span.bfx-price.bfx-list-price::text').get().replace('$',''),
            'description': f"{about}, {product_dna}" if about and product_dna else about or product_dna,
            'link': product_url
        }

    