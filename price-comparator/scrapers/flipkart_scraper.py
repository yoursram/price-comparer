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
        
        # Try finding individual product container class 'jIjQ8S' (list view) first
        product_div = soup.find('div', {'class': 'jIjQ8S'})
        
        # Fallback to the old list container DOjaWF
        if not product_div:
            product_div = soup.find('div', {'class': 'DOjaWF'})
            
        if not product_div:
            return None

        # Title: in list view, the title is inside class 'RG5Slk'
        title_tag = product_div.find(class_='RG5Slk')
        title = title_tag.text.strip() if title_tag else product_name

        # Price: search for updated class 'hZ3P6w' or standard 'Nx9bqj'
        price_tag = product_div.find(class_=lambda x: x and ('hZ3P6w' in x or 'Nx9bqj' in x))
        price = price_tag.text.strip() if price_tag else "Price not found"

        # Rating: search for updated class 'CjyrHS', 'MKiFS6', or standard 'XQDdHH'
        rating_tag = product_div.find(class_=lambda x: x and ('CjyrHS' in x or 'MKiFS6' in x or 'XQDdHH' in x))
        rating = rating_tag.text.strip() if rating_tag else "Rating not found"

        # Link: find first anchor tag inside product container
        link_tag = product_div.find('a', href=True)
        product_url = "https://www.flipkart.com" + link_tag['href'] if link_tag else "URL not found"

        return {
            "platform": "Flipkart",
            "title": title,  # Use the parsed title
            "price": price,
            "rating": rating,
            "url": product_url
        }

    except Exception as e:
        print(f"Flipkart scraping error: {e}")
        return None