import unittest
from utils.extract import extract_data
from bs4 import BeautifulSoup

class TestExtract(unittest.TestCase):
    def test_extract_valid_product(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Cool Shirt</h3>
            <img src="http://example.com/image.jpg"/>
            <span class="price">$100</span>
            <p>Rating: 4.5 / 5</p>
            <p>Size: M</p>
            <p>Color: Red</p>
            <p>Gender: Male</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find('div', class_='collection-card')
        result = extract_data(section)
        self.assertIsNotNone(result)
        self.assertEqual(result['product_name'], 'Cool Shirt')

    def test_extract_dirty_product(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Unknown Product</h3>
            <span class="price">Price Unavailable</span>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        section = soup.find('div', class_='collection-card')
        result = extract_data(section)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
