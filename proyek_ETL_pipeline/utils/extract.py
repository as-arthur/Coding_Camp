import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import time

headers = {
    "User-Agent" : (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
                    )
}

dirty_pattern = {
    "product_name": ["Unknown Product"],
    "rating" : ["Invalid Rating / 5", "Not Rated"],
    "price" : ["Price Unavailable", None]
}

def extract_data (section) :
    try:
        title_tag = section.find('h3', class_='product-title')
        product_name = title_tag.text.strip() if title_tag else "Unknown Product"

        img_tag = section.find('img')
        pict_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

        price_tag = section.find('span', class_='price')
        price = price_tag.text.strip() if price_tag else "Price Unavailable"

        # Inisialisasi default
        rating = color = size = gender = None

        for p in section.find_all('p'):
            text = p.text.strip()
            if "Rating:" in text:
                rating = text.split("Rating:")[-1].strip()
            elif "Color" in text:
                color = text
            elif "Size:" in text:
                size = text.split("Size:")[-1].strip()
            elif "Gender:" in text:
                gender = text.split("Gender:")[-1].strip()

        # Filter dirty
        if product_name in dirty_pattern["product_name"] or \
           rating in dirty_pattern["rating"] or \
           price in dirty_pattern["price"]:
            print(f"Produk dilewati karena dirty: {product_name}, {rating}, {price}")
            return None

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

        return {
            "product_name": product_name,
            "pict_url": pict_url,
            "rating": rating,
            "size": size,
            "color": color,
            "gender": gender,
            "price": price,
            "timestamp": timestamp
        }

    except Exception as e:
        import traceback
        print(f"Kesalahan ketika ekstraksi data: {e}")
        traceback.print_exc()
        return None



def fetch_page_content(url):
    
    session = requests.Session()
    response = session.get (url,headers=headers)
    try:
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print (f"terjadi kesalahan ketika melakukan request terhadap {url}:{e}")
        return None
    
def scrape (base_url, start_page=1, delay=2):
    data = []
    page_number = start_page

    while True:
        if page_number == 1:
            url = 'https://fashion-studio.dicoding.dev/'
        else:
            url = base_url.format(page_number)
            print(f"Scraping Halaman {url}")

        print (f"Halaman {url}")
        content = fetch_page_content(url)
        if content:
            soup = BeautifulSoup(content.text, "html.parser")
            section_element = soup.find_all("div", class_= "collection-card")
            for section in section_element:
                products = extract_data(section)
                if products:
                    data.append(products)

            next_button = soup.find('li', class_= 'page-item next')
            if next_button:
                page_number += 1
                time.sleep(delay)
            else:
                break
        else:
            print(f"gagal di halaman: {page_number}")
            break
    print (f"total data : {len(data)}")
    return data

def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_product = scrape(BASE_URL)
    df = pd.DataFrame(all_product)
    print(df)


if __name__ == '__main__':
    main()
    