import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred_data(
    api_key: str,
    series_id: str,
    observation_start: str = "1776-07-04",
    observation_end: str = "9999-12-31",
    limit: int = 100000,
    units: str = "lin",
    frequency: str = None,
    aggregation_method: str = "avg",
):
    """
    Fetch economic data from the FRED API with simplified parameters.

    Args:
        api_key (str): Your FRED API key.
        series_id (str): The FRED series ID.
        observation_start (str): Start date for observations (YYYY-MM-DD).
        observation_end (str): End date for observations (YYYY-MM-DD).
        limit (int): Maximum number of results to return (1-100000).
        units (str): Data value transformation. One of 'lin', 'chg', 'ch1', 'pch', 'pc1', 'pca', 'cch', 'cca', 'log'.
        frequency (str, optional): Lower frequency to aggregate data to. E.g., 'd', 'm', 'a'.
        aggregation_method (str): Aggregation method. One of 'avg', 'sum', 'eop'.

    Returns:
        list: A list of dictionaries with 'date' and 'value'.

    Raises:
        ValueError: If any parameter is invalid.
        requests.exceptions.RequestException: If the API request fails.
    """
    # Validate parameters
    valid_units = {"lin", "chg", "ch1", "pch", "pc1", "pca", "cch", "cca", "log"}
    if units and units not in valid_units:
        raise ValueError(f"Invalid units '{units}'. Must be one of: {', '.join(valid_units)}")

    valid_aggregation_methods = {"avg", "sum", "eop"}
    if aggregation_method not in valid_aggregation_methods:
        raise ValueError(f"Invalid aggregation_method '{aggregation_method}'. Must be one of: {', '.join(valid_aggregation_methods)}")

    # Build query parameters
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",  # Always use JSON
        "observation_start": observation_start,
        "observation_end": observation_end,
        "limit": limit,
        "units": units,
        "frequency": frequency or "",
        "aggregation_method": aggregation_method,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse observations
        observations = data.get("observations", [])
        return [{"date": obs["date"], "value": float(obs["value"])} for obs in observations]

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from FRED API: {e}")
        raise