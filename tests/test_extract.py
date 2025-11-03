import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Fix Import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import scrape_page

class TestExtract(unittest.TestCase):
    
    @patch('utils.extract.requests.get')
    def test_collect_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="collection-card">
                    <div class="product-details">
                        <h3 class="product-title">Outerwear 5</h3>
                        <span class="price">$15</span>
                        <p>Rating: 4 stars</p>
                        <p>Colors: Blue</p>
                        <p>Size: S</p>
                        <p>Gender: Women</p>
                    </div>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        result = scrape_page(1)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('Title', result[0])
        self.assertEqual(result[0]['Title'], 'Outerwear 5')
        self.assertEqual(result[0]['Price'], '$15')
        self.assertEqual(result[0]['Rating'], '4 stars')
        self.assertEqual(result[0]['Colors'], 'Colors: Blue')
        self.assertEqual(result[0]['Size'], 'Size: S')
        self.assertEqual(result[0]['Gender'], 'Gender: Women')

    @patch('utils.extract.requests.get')
    def test_collect_empty(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <body>
            </body>
        </html>
        """
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = scrape_page("http://example.com")
        
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()