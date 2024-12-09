from src.oura_data_handler import OuraDataHandler

# Define file paths and access token
address = "/path/to/localdata/"
data_files = {
    'daily_sleep': address + 'oura_daily-sleep.csv',
}
handler = OuraDataHandler(
    api_address="https://api.ouraring.com",
    local_data_paths=data_files,
    access_token="YOUR_ACCESS_TOKEN"
)

# Plot sleep data trends
handler.get_and_plot_daily_data(
    data_type="daily_sleep",
    source="csv",
    start_date="2023-11-01",
    duration="month",
    caption="Daily sleep trends over time.",
    detect_trends=True
)
