import unittest
from unittest.mock import patch
from fetch_fred_data import fetch_fred_data  # Adjust the import path as needed

class TestFetchFredData(unittest.TestCase):
    @patch("fetch_fred_data.requests.get")
    def test_fetch_fred_data_success(self, mock_get):
        # Arrange
        api_key = "dummy_api_key"
        series_id = "GDP"
        observation_start = "2020-01-01"
        observation_end = "2020-12-31"
        mock_response = {
            "observations": [
                {"date": "2020-01-01", "value": "100"},
                {"date": "2020-02-01", "value": "105"},
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Act
        data = fetch_fred_data(
            api_key=api_key,
            series_id=series_id,
            observation_start=observation_start,
            observation_end=observation_end,
            units="lin",
            frequency="m",
            aggregation_method="avg",
        )

        # Assert
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)  # Two records in mock response
        self.assertEqual(data[0]["date"], "2020-01-01")  # Check first record's date
        self.assertEqual(data[0]["value"], 100.0)  # Check first record's value

    def test_invalid_units(self):
        # Arrange
        api_key = "dummy_api_key"
        series_id = "GDP"
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            fetch_fred_data(
                api_key=api_key,
                series_id=series_id,
                units="invalid_unit"
            )
        self.assertIn("Invalid units", str(context.exception))

    def test_invalid_aggregation_method(self):
        # Arrange
        api_key = "dummy_api_key"
        series_id = "GDP"
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            fetch_fred_data(
                api_key=api_key,
                series_id=series_id,
                aggregation_method="invalid_method"
            )
        self.assertIn("Invalid aggregation_method", str(context.exception))

    @patch("fetch_fred_data.requests.get")
    def test_api_error(self, mock_get):
        # Arrange
        api_key = "dummy_api_key"
        series_id = "GDP"
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        # Act & Assert
        with self.assertRaises(requests.exceptions.RequestException):
            fetch_fred_data(api_key=api_key, series_id=series_id)

if __name__ == "__main__":
    unittest.main()
