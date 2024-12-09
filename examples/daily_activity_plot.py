import sys
sys.path.append('../')  # Replace with the path to the `src` directory

from src.oura_data_handler import OuraDataHandler

# Define file paths and access token
address = "/path/to/localdata/"
data_files = {
    'daily_activity': address + 'oura_daily-activity.csv',
}
handler = OuraDataHandler(
    api_address="https://api.ouraring.com",
    local_data_paths=data_files,
    access_token="YOUR_ACCESS_TOKEN"
)

# Plot daily activity from CSV
handler.get_and_plot_daily_data(
    data_type="daily_activity",
    source="csv",
    start_date="2023-11-01",
    duration="month",
    caption="Daily activity over time.",
    detect_trends=True,
    detect_anomalies=True
)
