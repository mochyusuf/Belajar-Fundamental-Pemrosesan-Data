import time
import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://fashion-studio.dicoding.dev"

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Avast Secure Browser";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Avast/141.0.0.0',
}
MAX_PAGES = 50
MAX_PAGES = 1

def scrape_page(page_number):
    products_on_page = []
    
    url = BASE_URL if page_number == 1 else f"{BASE_URL}/page{page_number}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        with open("response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        product_cards = soup.find_all('div', class_='collection-card')

        print(f"Product : {len(product_cards)}")
        for card in product_cards:
            product_details = {}

            title_tag = card.find("h3", class_="product-title")
            price_tag = card.find("span", class_="price")
            rating_tag = card.find("p", string=lambda text: text and "Rating:" in text)
            colors_tag = card.find("p", string=lambda text: text and "Colors" in text)
            size_tag = card.find("p", string=lambda text: text and "Size:" in text)
            gender_tag = card.find("p", string=lambda text: text and "Gender:" in text)

            title = title_tag.get_text(strip=True) if title_tag else None
            price = price_tag.get_text(strip=True) if price_tag else None
            rating = rating_tag.get_text(strip=True).replace("Rating: ", "") if rating_tag else None
            colors = colors_tag.get_text(strip=True) if colors_tag else None
            size = size_tag.get_text(strip=True) if size_tag else None
            gender = gender_tag.get_text(strip=True) if gender_tag else None

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            product_details['Title'] = title
            product_details['Price'] = price
            product_details['Rating'] = rating
            product_details['Colors'] = colors
            product_details['Size'] = size
            product_details['Gender'] = gender
            product_details['Timestamp'] = timestamp
            
            products_on_page.append(product_details)
    except requests.exceptions.RequestException as e:
        print(f"Error page {page_number}: {e}")
    except Exception as e:
        print(f"An unexpected error page {page_number}: {e}")
        
    return products_on_page

def extract_data():
    all_products = []
    
    print("Starting extract")
    for page in range(1, MAX_PAGES + 1):
        print(f"Scraping page {page}/{MAX_PAGES}...")
        products = scrape_page(page)
        if products:
            all_products.extend(products)
        time.sleep(1) 
    
    print(f"Found {len(all_products)} products.")

    df = pd.DataFrame(all_products)

    if df.empty:
        print("DataFrame is empty.")

    return df