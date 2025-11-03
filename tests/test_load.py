import unittest
from unittest.mock import patch, MagicMock, Mock
import pandas as pd
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import load_to_csv, load_to_gdrive, load_to_postgres
import tempfile

class TestLoad(unittest.TestCase):
    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        data = pd.DataFrame({
            "Title": ["Product A"],
            "Price": [160000.0],
            "Rating": [4.5],
            "Colors": [2],
            "Size": ["M"],
            "Gender": ["Unisex"],
            "timestamp": ["2024-01-01T00:00:00"]
        })

        file_path = os.path.join(os.getcwd(), 'test.csv')
        load_to_csv(data, file_path)
    
        mock_to_csv.assert_called_once_with(file_path, index=False)

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_load_to_gdrive(self, mock_creds, mock_build):
        data = pd.DataFrame({
            "Title": ["Product A"],
            "Price": [160000.0],
            "Rating": [4.5],
            "Colors": [2],
            "Size": ["M"],
            "Gender": ["Unisex"],
            "timestamp": ["2024-01-01T00:00:00"]
        })

        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        load_to_gdrive(data, "1caB8rcwPs0TNvMMxG3vnKRxM3IU3336JelqeU5MfTiU", "google-sheets-api.json")

        mock_build.assert_called_once()
        mock_creds.assert_called_once_with('google-sheets-api.json')
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    @patch('utils.load.create_engine')
    def test_load_to_postgres(self, mock_engine):
        df = pd.DataFrame({
            'Title': ['T-shirt 1', 'T-shirt 2'],
            'Price': [200000, 400000],
            'Rating': [4, 3],
            'Colors': [4, 2],
            'Size': ['S', 'M'],
            'Gender': ['Women', 'Men'],
            'Timestamp': ['2024-02-02 11:00:00', '2024-02-02 12:00:00']
        })
        
        mock_conn = MagicMock()
        mock_engine.return_value = mock_conn
    
        load_to_postgres(df, table_name='test')
        mock_conn.dispose.assert_not_called()

if __name__ == '__main__':
    unittest.main()