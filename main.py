from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


if __name__ == '__main__':
	spider_loader = SpiderLoader(get_project_settings())
	spiders = spider_loader.list()

	process = CrawlerProcess(get_project_settings())
	for spider in spiders:
		process.crawl(spider_loader.load(spider))
	process.start()