import scrapy

class ReebokScraper(scrapy.Spider):
    name = 'reebok'

    start_urls = [
        'https://reebok.ca/collections/mens-shoes?page=1',
        'https://reebok.ca/collections/mens-shoes?page=2',
        'https://reebok.ca/collections/mens-shoes?page=3',
        'https://reebok.ca/collections/mens-shoes?page=4',
        'https://reebok.ca/collections/mens-shoes?page=5',
        'https://reebok.ca/collections/mens-shoes?page=6',
        'https://reebok.ca/collections/womens-shoes?page=1',
        'https://reebok.ca/collections/womens-shoes?page=2',
        'https://reebok.ca/collections/womens-shoes?page=3',
        'https://reebok.ca/collections/womens-shoes?page=4',
        'https://reebok.ca/collections/womens-shoes?page=5',
        'https://reebok.ca/collections/womens-shoes?page=6',
        'https://reebok.ca/collections/kids-boys',
        'https://reebok.ca/collections/kids-girls',
    ]

    def parse(self, response):
        for link in response.css('li.collection-terminal-item.grid__item.product-item a::attr(href)'):
            url = response.urljoin(link.get())
            yield response.follow(url, callback = self.parse_deep, meta={'product_url': url})

        '''next_page = response.css('div.pagination-wrapper a::attr(href)').get()

        if next_page:
            next_page_url = response.urljoin(next_page)
            self.log(f"Next page URL: {next_page_url}")  # Add this line to log the next page URL
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.log("No next page found.")  # Log if no next page is found'''

    def parse_deep(self, response):
        product_url = response.meta['product_url']
        about = response.css('div.product__description-text::text').get()
        details = response.css('div.grid__item p.f-body.product__tag-detail--text span::text').getall()

        yield {
            'name': response.css('h2.h4.product__title.medium-up--hide::text').get(),
            'price': response.css('span.price-item.price-item--sale.price-item--last::text').get().strip().replace('$', ''),
            'description': f"{about}, {details}" if about and details else about or details,
            'link': product_url
        }