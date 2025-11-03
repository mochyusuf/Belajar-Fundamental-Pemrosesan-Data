import unittest
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    def test_transform_success(self):
        sample_data = {
            'Title': [
                'T-shirt 8', 
                'Hoodie 9',
            ],
            'Price': [
                '$ 50', 
                '$ 40',
            ],
            'Rating': [
                'Rating: ⭐ 4.0 / 5', 
                'Rating: ⭐ 3.0 / 5',
            ],
            'Colors': [
                '4 Colors', 
                '3 Colors',
            ],
            'Size': [
                'Size: M', 
                'Size: S', 
            ],
            'Gender': [
                'Gender: Women', 
                'Gender: Men',
            ],
            'Timestamp': [
                '2025-12-12 13:00:00', 
                '2025-13-13 13:00:00', 
            ]
        }
        raw_data = pd.DataFrame(sample_data)

        result = transform_data(raw_data)

        print(len(result))
        
        self.assertEqual(len(result), 2)

        test_columns = [
            'Title', 
            'Price', 
            'Rating', 
            'Colors', 
            'Size', 
            'Gender', 
            'Timestamp'
        ]
        self.assertEqual(list(result.columns),test_columns)
        
        first_row = result.iloc[0]
        self.assertEqual(first_row['Title'],'T-shirt 8')
        self.assertEqual(first_row['Price'],(50 * 16000))
        self.assertEqual(first_row['Rating'],4)
        self.assertEqual(first_row['Colors'],4)
        self.assertEqual(first_row['Size'],'M')
        self.assertEqual(first_row['Gender'],'Women')

    def test_transform_duplicate(self):
        sample_data = {
            'Title': [
                'T-shirt 8', 
                'T-shirt 8', 
            ],
            'Price': [
                '$50', 
                '$50', 
            ],
            'Rating': [
                'Rating: ⭐ 4.0 / 5', 
                'Rating: ⭐ 4.0 / 5', 
            ],
            'Colors': [
                '4 Colors', 
                '4 Colors', 
            ],
            'Size': [
                'Size: M', 
                'Size: M', 
            ],
            'Gender': [
                'Gender: Women', 
                'Gender: Women', 
            ],
            'Timestamp': [
                '2025-11-11 13:00:00', 
                '2025-11-11 13:00:00', 
            ]
        }
        raw_data = pd.DataFrame(sample_data)

        result = transform_data(raw_data)
        
        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()