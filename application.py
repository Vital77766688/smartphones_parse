import os
import json
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


OUTPUT_PATH = 'output/'


def prepare_data():
	files = os.listdir(OUTPUT_PATH)
	data = []
	for file in files:
		with open(os.path.join(OUTPUT_PATH, file), 'rb') as f: 
			data += json.loads(f.read())
	data = sorted(data, key=lambda x: x['price'])
	return data


@app.template_filter()
def price(text):
	return "{:,} KZT".format(text).replace(',',' ')


@app.route('/', methods=['GET'])
def index():
	data = prepare_data()	
	return render_template('index.html', context={'data': data[0:20]})


@app.route('/get_more', methods=['GET'])
def get_more():
	limit = request.args.get('limit', type=int) or 20
	offset = request.args.get('offset', type=int) or 0
	data = prepare_data()
	return jsonify(data[offset:offset+limit]), 200