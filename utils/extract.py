import time, requests
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_url_content(url):
    """Fetch HTML Content from url"""
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()

        if response.status_code == 404:
            return None
        
        return response.content
    except requests.exceptions.Timeout:
        print("Timeout Error while making requests to {}".format(url))
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error when making requests to {url}: {e}")
        return None
    except Exception as e:
        print(f"An Error occyreed while scraping {url}: {e}")
        return None
    
def scrape_products(url, start_page=1, delay=1):
    """Make request to website, get all products, and save to a variable"""
    products = []
    page = start_page

    while True:
        if (page != start_page):
            url = url.replace("/page{}".format(page-1), "")
            url = url + "/page{}".format(page) 
        print("Scraping: ", url)

        content = fetching_url_content(url)

        if content:
            try:
                soup = BeautifulSoup(content, "html.parser")
                div_cards = soup.find_all("div", {"class": "collection-card"})

                for card in div_cards:
                    timestamp = datetime.now().isoformat()
                    product = parse_product_details(card, timestamp)
                    products.append(product)

                is_nextPage = soup.find('a', {"class": "page-link"})
                if is_nextPage:
                    page += 1
                    time.sleep(delay)
                else:
                    break
            except AttributeError as e:
                print(f"Attribute error occured while parsing page {page}: {e}")
            except Exception as e:
                print(f"Error parsing page {url}: {e}")
                break
        else:
            break

    return products


def parse_product_details(card, timestamp):
    """Parse html to get product details (Title, Price, Rating, Colors, Size, Gender)"""
    try:
        title = card.find("h3", {"class": "product-title"}).text
    except Exception as e:
        title = "Title Unavailable"
        print(f"Error while parsing product title: {e}")

    try:
        price_element = card.find("span", class_='price')
        if not price_element:
            price_element = card.find("p", class_='price')
        price = price_element.text.strip()
    except(AttributeError) as e:
        price = "Price Unavailable"
        print("Error while parsing product price: {}".format(e))

    try:
        additional_infos = card.find_all("p", {"style": "font-size: 14px; color: #777;"})
        rating = additional_infos[0].text.strip()  
        colors = additional_infos[1].text.strip()  
        size = additional_infos[2].text.strip()   
        gender = additional_infos[3].text.strip() 
    except (IndexError, ValueError) as e:
        rating, colors, size, gender = "Not Rated", "Unknown Colors", "Unknown Size", "Unknown Gender"
        print(f"Warning: Some product details (rating, colors, size, gender) are missing. Error: {e}")

    product = {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
        "Timestamp": timestamp
    }

    return product