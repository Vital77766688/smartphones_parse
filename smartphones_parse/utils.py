import logging


def clean_title(value, string_to_replace):
	return value.replace(string_to_replace,'').strip()


def clean_price(value, url):
	try:
		cleaned = ''.join([s for s in value if s.isdigit()])
		if cleaned == '':
			raise TypeError	

		return int(cleaned)

	except TypeError:
		logging.warning(f'Price for this url {url} was not parsed')
		return None
