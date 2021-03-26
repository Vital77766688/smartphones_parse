import json
import re
from math import ceil

import scrapy

from ..utils import clean_price, clean_title


def get_url_from_style(value):
	return re.search('(url\(\')(.*)(\'\))', value).group(2)


class BeliyVeterSpider(scrapy.Spider):
	name = 'beliy_veter'

	start_urls = [
		'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply'
	]

	def parse(self, response):
		for item in response.css('div.bx_catalog_item'):
			data = {
				'url': response.urljoin(item.css('div.bx_catalog_item_title a::attr(href)').get()),
				'title': clean_title(item.css('div.bx_catalog_item_title a::text').get(), 'Смартфон'),
				'price': clean_price(
					item.css(
						'div.bx_catalog_item_price div.bx_price div.bx-more-prices ul li span.bx-more-price-text::text'
					)\
					.getall()[-1]
				),
				'image': response.urljoin(
					get_url_from_style(
						item.css(
							'figure.item_image_container a.bx_catalog_item_images::attr(style)'
						).get()
					)
				),
				'shop': 'Beliy Veter'
			}
			yield data

		next_page = response.css('div.bx-pagination-container ul li.bx-pag-next a::attr(href)').get()
		if next_page:
			yield response.follow(next_page, callback=self.parse)