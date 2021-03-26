import json
from math import ceil

import scrapy

from ..utils import clean_price, clean_title


class MechtaKzSpider(scrapy.Spider):
	name = 'mechta.kz'

	def start_requests(self):
		url = 'https://www.mechta.kz/api/main/catalog_new/?section=smartfony&filter=true&setcity=al'
		yield scrapy.Request(url, callback=self.parse_filters)

	def parse_filters(self, response):
		total_items = json.loads(response.body)['data']['all']
		items_per_page = 18
		page_count = ceil(total_items/items_per_page)
		for page in range(1, page_count+1):
			url = f"https://www.mechta.kz/api/main/catalog_new/?section=smartfony&page_num={page}&catalog=true&page_element_count={items_per_page}&setcity=al"
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		data = json.loads(response.body)
		for item in data['data']['ITEMS']:
			yield {
				'url': f"https://mechta.kz/product/{item['CODE']}/",
				'title': clean_title(item['NAME'], 'Телефон сотовый'),
				'price': item['PRICE']['PRICE'],
				'image': item['PHOTO'][0] if len(item['PHOTO']) else '',
				'shop': 'Mechta.kz'
			}
