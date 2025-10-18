import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

def scrape_flipkart(product_name):
    """Scrapes Flipkart for a given product and returns its details."""
    try:
        formatted_query = "+".join(product_name.split())
        url = f"https://www.flipkart.com/search?q={formatted_query}"
        
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "lxml")
        
        product_div = soup.find('div', {'class': 'DOjaWF'})
        if not product_div:
            return None

        # Title scraping logic is no longer needed

        price_tag = product_div.find('div', {'class': 'Nx9bqj'})
        price = price_tag.text.strip() if price_tag else "Price not found"

        rating_tag = product_div.find('div', {'class': 'XQDdHH'})
        rating = rating_tag.text.strip() if rating_tag else "Rating not found"

        link_tag = product_div.find('a', {'class': 'wU_t2p'})
        product_url = "https://www.flipkart.com" + link_tag['href'] if link_tag else "URL not found"

        return {
            "platform": "Flipkart",
            "title": product_name,  # Use the user's input directly as the title
            "price": price,
            "rating": rating,
            "url": product_url
        }

    except Exception as e:
        print(f"Flipkart scraping error: {e}")
        return None