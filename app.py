from flask import Flask, jsonify, request
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch HTML content using a proxy
def fetch_html_content(url):
    proxy_params = {
        'api_key': '',  # Replace with your actual API key
        'url': url,
    }

    response = requests.get(
        url='https://proxy.scrapeops.io/v1/',
        params=proxy_params,
        timeout=120,
    )

    return response.content

@app.route('/fetch_product_data', methods=['GET'])
def fetch_product_data():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    # Fetch HTML content
    html_content = fetch_html_content(url)

    # Initialize BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract ld+json data
    ld_json_script = soup.find('script', type='application/ld+json')
    ld_json_data = json.loads(ld_json_script.string) if ld_json_script else {}

    # Extract relevant information
    data = {
        'product_name': ld_json_data.get('name'),
        'description': ld_json_data.get('description'),
        'brand': ld_json_data.get('brand', {}).get('name'),
        'offers_url': ld_json_data.get('offers', {}).get('url'),
        'price_currency': ld_json_data.get('offers', {}).get('priceCurrency'),
        'price': ld_json_data.get('offers', {}).get('price'),
        'rating_value': ld_json_data.get('aggregateRating', {}).get('ratingValue'),
        'review_count': ld_json_data.get('aggregateRating', {}).get('reviewCount'),
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
