import pytest
import pandas as pd
import sys
sys.path.append('../')  # Replace with the path to the `src` directory
from src.oura_data_handler import OuraDataHandler
from datetime import datetime

@pytest.fixture
def handler():
    address = "../data"
    data_files = {
        'bedtime': address + 'oura_bedtime_2023-12-02T18-27-40.csv',
        'daily_activity': address + 'oura_daily-activity_2023-12-02T18-26-47.csv',
        'daily_readiness': address + 'oura_daily-readiness_2023-12-02T18-26-18.csv',
        'daily_sleep': address + 'oura_daily-sleep_2023-12-02T18-26-04.csv',
        'daily_spo2': address + 'oura_daily-spo2_2023-12-02T18-28-13.csv',
        'heart_rate': address + 'oura_heart-rate_2023-12-02T18-27-04.csv',
        'sleep': address + 'oura_sleep_2023-12-02T18-25-22.csv',
        'smoothed_location': address + 'oura_smoothed-location_2023-12-02T18-27-58.csv'
    }
    return OuraDataHandler(
        api_address="https://api.ouraring.com",
        local_data_paths=data_files,
        access_token="YOUR_ACCESS_TOKEN"
    )

def test_convert_date(handler):
    assert handler._convert_date("2023-12-08", "week") == "2023-12-04"
    assert handler._convert_date("2023-12-08", "day") == "2023-12-09"

def test_load_data_from_csv(handler):
    df = handler.load_data_from_csv('daily_sleep', '2023-11-01', duration='month')
    assert not df.empty
    assert 'day' in df.columns

def test_fetch_data_from_api(handler):
    # Assumes the access token is valid and the API is accessible
    df = handler.fetch_data_from_api('daily_sleep', '2023-11-01', duration='month')
    assert isinstance(df, pd.DataFrame)

def test_plot_data(handler):
    # Test plotting with a sample dataframe
    data = {
        'day': ['2023-11-01', '2023-11-02', '2023-11-03'],
        'score': [75, 80, 78]
    }
    df = pd.DataFrame(data)
    handler.plot_data(df, column='score', title='Test Plot')
