import csv
import requests
from bs4 import BeautifulSoup

def get_amazon_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product name
        product_name = soup.find('span', id='productTitle').get_text().strip()

        # Extract product image URL
        product_image = soup.find('div', id='imgTagWrapperId').find('img')['src']

        # Extract reviews
        reviews = []
        review_elements = soup.find_all('div', class_='review')
        for review in review_elements:
            review_text = review.find('span', class_='review-text').get_text().strip()
            reviews.append(review_text)

        return product_name, product_image, reviews
    else:
        print("Failed to fetch product information.")
        return None, None, []

def save_product_info_to_csv(product_name, product_image, reviews, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', 'Product Image', 'Review'])
        for review in reviews:
            writer.writerow([product_name, product_image, review])



