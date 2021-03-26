import scrapy

from ..utils import clean_price, clean_title


class ForaKzSpider(scrapy.Spider):
	name = 'fora.kz'

	start_urls = [
		'https://fora.kz/catalog/smartfony-plansety/smartfony/almaty'
	]

	def parse(self, response):
		for item in response.css('div.catalog-list-item'):
			if item.css('.injectable-banner'):
				continue
			data = {
				'url': response.urljoin(item.css('div.item-info a::attr(href)').get()),
				'title': clean_title(item.css('div.item-info a::text').get(), 'Смартфон'),
				'price': clean_price(item.css('div.item-price p.price::text').get()),
				'image': item.css('div.image img::attr(src)').get(),
				'shop': 'Fora.kz'
			}
			yield data

		next_page = response.css('ul.pagination li a::attr(href)').getall()[-1]
		if next_page:
			yield response.follow(next_page, callback=self.parse)
