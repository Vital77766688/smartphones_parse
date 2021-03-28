import json
from math import ceil

import chompjs

import scrapy
from scrapy_selenium import SeleniumRequest

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
			yield scrapy.Request(url=url, callback=self.parse_pages)

	def parse_pages(self, response):
		data = json.loads(response.body)
		for item in data['data']['ITEMS']:
			url = f"https://mechta.kz/product/{item['CODE']}/"
			yield SeleniumRequest(url=url, callback=self.parse_details)

	def parse_details(self, response):

		scripts = response.css('script::text').getall()
		for script in scripts:
			try:
				obj = chompjs.parse_js_object(script)
				if 'product' in obj:
					obj = obj['product']['preFetchedData']
					break
			except ValueError as e:
				pass

		data = {
			'shop': 'mechta.kz',
			'url': response.request.url,
			'title': clean_title(obj['NAME'], 'Телефон сотовый'),
			'price': obj['PRICE']['PRICE'],
			'images': obj['PHOTO'],
			'specs': self.get_specs(obj)
		}
		yield data

	def get_specs(self, obj):
		data = {}
		for item in obj['PROPERTIES'].values():
			spec_category = item['PROP_GROUP_NAME']
			data[spec_category] = {}
			for spec in item['VALUES']:
				data[spec_category][spec['PROP_NAME']] = spec['PROP_VALUE']
		return data
