import os
import json
from datetime import datetime

from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter


class JsonWriterPipeline:
	def open_spider(self, spider):
		dt = datetime.now().strftime('%Y%m%d%H%M%S')
		filename = os.path.join(f'output/{spider.name}_{dt}.json')
		self.file = open(filename, 'wb')
		self.exporter = JsonItemExporter(self.file, encoding='utf-8')
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(ItemAdapter(item).asdict())
		return item
