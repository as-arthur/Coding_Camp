import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests

from utils.extract import extract_data, fetch_page_content, scrape

class TestExtractFunctions(unittest.TestCase):
    
    def setUp(self):
        self.valid_html = '''
        <div class="collection-card">
            <h3 class="product-title">Cool Jacket</h3>
            <img src="http://example.com/image.jpg" />
            <span class="price">$19.99</span>
            <p>Rating: ⭐ 4.2 / 5</p>
            <p>Color: Blue</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        '''
        self.dirty_html = '''
        <div class="collection-card">
            <h3 class="product-title">Unknown Product</h3>
            <span class="price">Price Unavailable</span>
            <p>Rating: Not Rated</p>
        </div>
        '''
    
    def test_extract_data_valid(self):
        soup = BeautifulSoup(self.valid_html, 'html.parser')
        section = soup.find('div', class_='collection-card')
        result = extract_data(section)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['product_name'], 'Cool Jacket')
        self.assertEqual(result['price'], '$19.99')
        self.assertIn('timestamp', result)

    def test_extract_data_dirty(self):
        soup = BeautifulSoup(self.dirty_html, 'html.parser')
        section = soup.find('div', class_='collection-card')
        result = extract_data(section)
        self.assertIsNone(result)
    
    @patch('utils.extract.requests.Session.get')
    def test_fetch_page_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        url = 'http://example.com'
        response = fetch_page_content(url)
        self.assertEqual(response.status_code, 200)

    @patch('utils.extract.requests.Session.get')
    def test_fetch_page_content_fail(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        url = 'http://example.com'
        response = fetch_page_content(url)
        self.assertIsNone(response)

    @patch('utils.extract.fetch_page_content')
    def test_scrape_single_page(self, mock_fetch):
        # Buat dummy HTML satu halaman dengan satu produk valid
        html = f"<html><body>{self.valid_html}</body></html>"
        mock_response = MagicMock()
        mock_response.text = html
        mock_fetch.return_value = mock_response

        base_url = 'http://example.com/page{}'
        result = scrape(base_url, start_page=1, delay=0)
        self.assertTrue(len(result) >= 1)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]['product_name'], 'Cool Jacket')


if __name__ == '__main__':
    unittest.main()
