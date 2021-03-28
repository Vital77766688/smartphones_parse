import scrapy

from ..utils import clean_price, clean_title


class ForaKzSpider(scrapy.Spider):
	name = 'fora.kz'

	def start_requests(self, **kwargs):
		url = 'https://fora.kz/catalog/smartfony-plansety/smartfony/almaty'
		yield scrapy.Request(url=url, callback=self.parse_pages)

	def parse_pages(self, response, **kwargs):
		for item in response.css('div.catalog-list-item'):
			if item.css('.injectable-banner'):
				continue
			url = response.urljoin(item.css('div.item-info a::attr(href)').get())
			yield scrapy.Request(url=url, callback=self.parse_details)

		next_page = response.css('ul.pagination li a::attr(href)').getall()[-1]
		if next_page:
			yield response.follow(next_page, callback=self.parse_pages)

	def parse_details(self, response, **kwargs):
		data = {
			'shop': 'fora.kz',
			'url': response.request.url,
			'title': clean_title(
				response.css('h1[itemprop="name"]::text').get(),''
			),
			'price': clean_price(
				response.css('div.price span[itemprop="price"]').get(),
				response.request.url
			),
			'images': response.css('div#product-gallery div#thumbs img::attr(src)').getall(),
			'specs': self.get_specs(response),
		}
		yield data

	def get_specs(self, response):
		data = {}
		for item in response.css('div.specifications-panel'):
			spec_category = item.css('h4::text').get().strip()
			data[spec_category] = {}
			for spec in item.css('table tr'):
				data[spec_category][spec.css('th::text').get().strip()] = spec.css('td::text').get().strip()
		return data