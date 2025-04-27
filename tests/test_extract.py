import unittest
from unittest.mock import patch, Mock
import requests
from bs4 import BeautifulSoup
from utils.extract import fetching_url_content, scrape_products,parse_product_details

class TestExtractFunctions(unittest.TestCase):

    @patch('utils.extract.requests.Session.get')
    def test_fetching_url_content_success(self, mock_get):
        """Test if the content is fetched succesfully"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><body>HTML content here</body></html>'
        mock_get.return_value = mock_response

        content = fetching_url_content("https://test.com")

        self.assertIsNotNone(content)
        self.assertEqual(content, b'<html><body>HTML content here</body></html>')

    @patch('utils.extract.requests.Session.get')
    def test_fetching_url_content_timeout(self, mock_get):
        """Test if a Timeout exception is caught and handled properly."""
        mock_get.side_effect = requests.exceptions.Timeout

        content = fetching_url_content("https://test.com")

        self.assertIsNone(content)

    @patch('utils.extract.requests.Session.get')
    def test_fetching_url_content_request_exception(self, mock_get):
        """Test if request exceptions is caught."""
        mock_get.side_effect = requests.exceptions.RequestException("Error")
        
        content = fetching_url_content("https://test.com")

        self.assertIsNone(content)

    @patch('utils.extract.requests.Session.get')
    def test_fetching_url_content_general_exception(self, mock_get):
        """Test general exception handling during fetching."""
        mock_get.side_effect = Exception("General Error")

        content = fetching_url_content("https://test.com")

        self.assertIsNone(content)
    
    @patch('utils.extract.requests.Session.get')
    def test_fetching_url_content_invalid_status_code(self, mock_get):
        """Test if the fetching_url_content handles invalid status code properly."""
        mock_response = Mock()
        mock_response.status_code = 404  # Simulating a 404 error
        mock_get.return_value = mock_response

        content = fetching_url_content("https://test.com/invalid")

        self.assertIsNone(content)




    def test_parse_product_details(self):
        """Test parsing product details from HTML card."""
        html_content = """
        <div class="collection-card">
            <div style="position: relative;">
                <img alt="T-shirt 2" class="collection-image" src="https://picsum.photos/280/350?random=2"/>
            </div>
            <div class="product-details">
                <h3 class="product-title">T-shirt 2</h3>
                <div class="price-container"><span class="price">$102.15</span></div>
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 3.9 / 5</p>
                <p style="font-size: 14px; color: #777;">3 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: M</p>
                <p style="font-size: 14px; color: #777;">Gender: Women</p>
            </div>
        </div>
        """

        soup = BeautifulSoup(html_content, "html.parser")
        card = soup.find("div", class_="collection-card")
        timestamp = "2025-04-27T12:00:00"

        result = parse_product_details(card, timestamp)

        self.assertEqual(result['Title'], "T-shirt 2")
        self.assertEqual(result['Price'], "$102.15")
        self.assertEqual(result['Rating'], "Rating: ⭐ 3.9 / 5")
        self.assertEqual(result['Colors'], "3 Colors")
        self.assertEqual(result['Size'], "Size: M")
        self.assertEqual(result['Gender'], "Gender: Women")
        self.assertEqual(result['Timestamp'], timestamp)

    def test_parse_product_details_missing_fields(self):
        """Test parsing product details when some fields are missing."""
        html_content = """
        <div class="collection-card">
            <div class="product-details">
                <!-- Missing title and price -->
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.5 / 5</p>
                <p style="font-size: 14px; color: #777;">5 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: L</p>
                <p style="font-size: 14px; color: #777;">Gender: Men</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html_content, "html.parser")
        card = soup.find("div", class_="collection-card")
        timestamp = "2025-04-27T12:00:00"

        result = parse_product_details(card, timestamp)

        self.assertIn('Title', result) 
        self.assertEqual(result['Title'], "Title Unavailable")
        self.assertIn('Price', result)
        self.assertEqual(result['Price'], "Price Unavailable")
        
        self.assertEqual(result['Rating'], "Rating: ⭐ 4.5 / 5")
        self.assertEqual(result['Colors'], "5 Colors")
        self.assertEqual(result['Size'], "Size: L")
        self.assertEqual(result['Gender'], "Gender: Men")
        self.assertEqual(result['Timestamp'], timestamp)

    def test_parse_product_details_no_additional_info(self):
        """Test parsing product details when no additional info <p> tags exist."""
        html_content = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">T-Shirt 2</h3>
                <span class="price">$10.00</span>
                <!-- No additional <p> info -->
            </div>
        </div>
        """
        soup = BeautifulSoup(html_content, "html.parser")
        card = soup.find("div", class_="collection-card")
        timestamp = "2025-04-27T12:00:00"

        result = parse_product_details(card, timestamp)

        self.assertEqual(result['Title'], "T-Shirt 2")
        self.assertEqual(result['Price'], "$10.00")
        self.assertEqual(result['Rating'], "Not Rated")
        self.assertEqual(result['Colors'], "Unknown Colors")
        self.assertEqual(result['Size'], "Unknown Size")
        self.assertEqual(result['Gender'], "Unknown Gender")

    def test_parse_product_details_price_in_p_tag(self):
        """Test parsing product price when price is in <p> tag instead of <span>."""
        html_content = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">P Price Product</h3>
                <p class="price">Price Unavailable</p>
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.8 / 5</p>
                <p style="font-size: 14px; color: #777;">4 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: L</p>
                <p style="font-size: 14px; color: #777;">Gender: Women</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html_content, "html.parser")
        card = soup.find("div", class_="collection-card")
        timestamp = "2025-04-27T12:00:00"

        result = parse_product_details(card, timestamp)

        self.assertEqual(result['Price'], "Price Unavailable")




    @patch("utils.extract.fetching_url_content")
    def test_scrape_products_success(self, mock_fetching_url_content):
        """Test scraping products from the website."""
        html_content = """
        <html>
            <body>
                <div class="collection-card">
                    <div style="position: relative;">
                        <img alt="T-shirt 2" class="collection-image" src="https://picsum.photos/280/350?random=2"/>
                    </div>
                    <div class="product-details">
                        <h3 class="product-title">T-shirt 2</h3>
                        <div class="price-container"><span class="price">$102.15</span></div>
                        <p style="font-size: 14px; color: #777;">Rating: ⭐ 3.9 / 5</p>
                        <p style="font-size: 14px; color: #777;">3 Colors</p>
                        <p style="font-size: 14px; color: #777;">Size: M</p>
                        <p style="font-size: 14px; color: #777;">Gender: Women</p>
                    </div>
                </div>
            </body>
        </html>
        """
        mock_fetching_url_content.return_value = html_content.encode('utf-8')

        products = scrape_products("https://test.com", start_page=1, delay=0)

        self.assertEqual(len(products), 1)
        product = products[0]

        self.assertEqual(product['Title'], "T-shirt 2")
        self.assertEqual(product['Price'], "$102.15")
        self.assertEqual(product['Rating'], "Rating: ⭐ 3.9 / 5")
        self.assertEqual(product['Colors'], "3 Colors")
        self.assertEqual(product['Size'], "Size: M")
        self.assertEqual(product['Gender'], "Gender: Women")
        self.assertIn('Timestamp', product)

    @patch("utils.extract.fetching_url_content")
    def test_scrape_products_fetch_failure(self, mock_fetching_url_content):
        """Test scrape_products when fetching_url_content returns None (fetch failure)."""
        mock_fetching_url_content.return_value = None

        products = scrape_products("https://test.com", start_page=1, delay=0)

        self.assertEqual(products, [])

    @patch("utils.extract.fetching_url_content")
    def test_scrape_products_parse_exception(self, mock_fetching_url_content):
        """Test scrape_products when parsing HTML fails."""
        html_content = "<html><body><div>No collection-card here</div></body></html>"
        mock_fetching_url_content.return_value = html_content.encode('utf-8')

        products = scrape_products("https://test.com", start_page=1, delay=0)

        self.assertEqual(products, [])

    @patch("utils.extract.fetching_url_content")
    def test_scrape_products_no_next_page(self, mock_fetching_url_content):
        """Test scrape_products stopping when there is no next page link."""
        html_content = """
        <html>
            <body>
                <div class="collection-card">
                    <div class="product-details">
                        <h3 class="product-title">Product 1</h3>
                        <span class="price">$10</span>
                        <p style="font-size: 14px; color: #777;">Rating: ⭐ 5.0 / 5</p>
                        <p style="font-size: 14px; color: #777;">1 Color</p>
                        <p style="font-size: 14px; color: #777;">Size: S</p>
                        <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
                    </div>
                </div>
                
            </body>
        </html>
        """
        mock_fetching_url_content.return_value = html_content.encode('utf-8')

        products = scrape_products("https://test.com", start_page=1, delay=0)

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['Title'], "Product 1")

    @patch("utils.extract.fetching_url_content")
    @patch("utils.extract.BeautifulSoup")
    def test_scrape_products_general_parsing_exception(self, mock_beautifulsoup, mock_fetching_url_content):
        """Test scrape_products when general Exception occurs during parsing."""
        html_content = "<html><body>something</body></html>"
        mock_fetching_url_content.return_value = html_content.encode('utf-8')

        mock_soup = Mock()
        mock_soup.find_all.side_effect = Exception("Mocked general parsing error")
        mock_beautifulsoup.return_value = mock_soup

        products = scrape_products("https://test.com", start_page=1, delay=0)
        self.assertEqual(products, [])