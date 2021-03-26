def clean_title(value, string_to_replace):
	return value.replace(string_to_replace,'').strip()


def clean_price(value):
	cleaned = ''.join([s for s in value if s.isdigit()])
	if cleaned:
		return int(cleaned)
	return None