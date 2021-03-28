import json
import re
from math import ceil

import scrapy

from ..utils import clean_price, clean_title

"""
TODO: Обработать сообщение "Этот товар уже закончился"
"""


def get_url_from_style(value):
	return re.search('(url\(\')(.*)(\'\))', value).group(2)


class BeliyVeterSpider(scrapy.Spider):
	name = 'beliy_veter'

	def start_requests(self, **kwargs):
		url = 'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply'
		yield scrapy.Request(url=url, callback=self.parse_pages)

	def parse_pages(self, response, **kwargs):
		for item in response.css('div.bx_catalog_item'):
			url = response.urljoin(item.css('div.bx_catalog_item_title a::attr(href)').get())
			yield scrapy.Request(url=url, callback=self.parse_details)

		next_page = response.css('div.bx-pagination-container ul li.bx-pag-next a::attr(href)').get()
		if next_page:
			yield response.follow(next_page, callback=self.parse_pages)

	def parse_details(self, response, **kwargs):
		data = {
			'shop': 'Beliy Veter',
			'url': response.request.url,
			'title': clean_title(
				response.css('h1#pagetitle::text').get(),'Смартфон'
			),
			'price': clean_price(
				response.css('div.item_price div.item_current_price::text').get(),
				response.request.url
			),
			'images': [
				response.urljoin(
					get_url_from_style(item)
				) for item in response.css('div.bx_slide li span::attr(style)').getall()
			],
			'specs': self.get_specs(response)
		}

		yield data

	def get_specs(self, response):
		data = {}
		for item in response.css('div.bx_detail_chars_i'):
			name = item.css('dt.bx_detail_chars_i_title span::text').get().strip()
			value = item.css('dd.bx_detail_chars_i_field *::text').get().strip()
			data[name] = value
		return data
