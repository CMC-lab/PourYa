---
title: "PourYa: A Unified Library for Handling and Visualizing Oura Ring Data"
authors:
  - name: "Ali Mohammadi"
    affiliation: "Student of Tehran University"
  - name: "Prof. Shervin Safavi"
    affiliation: "Univ"
date: "2025-02-14"
---

## Summary

Stand is an open-source Python library that aims to accommodate the acquisition, processing, and visualization of data from the Oura Ring. By exposing a single unified interface to API-based and CSV-based ingestion, *PourYa* makes it easier for researchers and practitioners to explore a variety of wearable metrics, from sleep patterns to daily activity to heart rate variation. The core function of this package also contains advanced analytics like trend detection via change point analysis and anomaly detections, thus making it suitable for digital healthcare research and personal wellness analytics.

## Statement of Need

Wearable devices such as the Oura Ring have revolutionized personal health monitoring by generating elaborate datasets regarding sleep patterns, activity levels, heart rate, etc. However, researchers and practitioners face several difficulties in processing and analyzing this data:

- **Complex Data Pipelines:** Existing workflows for the extraction, cleaning, and visualization of wearable data often necessitate bespoke scripts along with manual outlining and integration of several libraries. This fosters higher chances of errors and limits the reproducibility of findings.
  
- **Data Accessibility:** The Oura API and local CSV exports certainly provide valuable metrics, but to extract meaningful insights from the raw data, a researcher needs to possess considerable programming skills. Such processes might easily intimidate researchers with neither a strong background nor exposure to data science.

- **Lack of Integrated Solutions:** There is an open space for a unified, open-source tool that presents a configurable toolkit for the whole data handling process—from fetching and processing data to performing trend analysis and anomaly detection—through well-known Python libraries. This could lessen the challenges currently faced by entry for researchers and take the rapid prototyping for analytical workflows to the next level.

*PourYa* addresses the explained challenges by providing a one-stop solution to accessing and visualizing the Oura Ring data. The benefits of the most popular libraries (pandas, matplotlib, ruptures, etc.) include enhanced workflow efficiency with the processing of data, trend analysis, and visualization within the PourYa's framework where consistency and reproducibility are absolute essentials. This inclusion will permit users to simply glean actionable insights and conclusions from the wearable data to promote improved research reproducibility and quicken the pursuit for progress in digital health. 


## Functionality and Implementation

*PourYa* is an open-source Python library meant to facilitate Oura Ring data processing and visualization. The entire workflow from data acquisition to final visualization is wrapped around the class called OuraDataHandler, aimed at an intuitive and consistent user experience.


### Core Functionalities

- **Data Acquisition:**  
  *PourYa* can obtain data directly from the Oura API or from locally stored CSV files. Fetching data from the API is done by the `fetch_data_from_api` method while loading a previously saved file is done with `load_data_from_csv`, which filters data based on the date range specified.
  
- **Date Handling:**  
  A specific method, `_convert_date`, allows the user to manipulate specific periods (i.e., days, weeks, months, or years) for generating queries to retrieve data over a rolling time frame.
  
- **Visualization:**  
  Various plot methods are made available for different analytical purposes:
  - `plot_data`, with custom line plots, automatically attempts detection of trend (using the *ruptures* package) and anomaly highlighting;
  - `plot_sleep_phases` visually plots various sleep stages in 5-minute intervals, converting the phase numbers into a more easily identifiable colored graph;
  - `plot_bedtime` and `plot_heart_rate` are aimed at understanding patterns related to going to bed and heart rate, respectively.


- **Trend and Anomaly Detection:**  
  Using *ruptures*, *PourYa*  marks change points for time series data that represent significant shifts in the metrics. Z-scores through rolling statistics have been utilized to flag potential outliers that are likely anomalies.


### Implementation Details

- **Class-Based Structure:**  
  The functional structure of this class, known as the **OuraDataHandler** class, allows extensibility and integration in data processing pipelines. Its constructor takes arguments in the form of API credentials and paths to local CSV that provide flexibility in locating the data.


- **Robust Data Handling:**  
  Date filtering is done based on the date ranges that the user supplies, with error-handling capabilities that allow missing or incorrect parameters. This ensures that only valid data makes it through for filtering and visualization. 


- **Integration with Established Libraries:**  
  By building on top of widely used Python libraries—such as `pandas` for data manipulation, `matplotlib` for plotting, and `ruptures` for change point detection—*PourYa* delivers both performance and familiarity, fostering rapid adoption in existing workflows.

- **Modular and Extensible Design:**  
*PourYa*, with distinct methods to do each job, is done in order to enhance the readability and maintainability of code while allowing other contributors to extend functionalities by a minimum rewriting effort (for example, by adding new metrics or visualization techniques).

## Example Usage

Below is an example of how to call PourYa to retrieve sleep data from a local CSV file and visualize it, as well as do a similar for daily activity data from the API, with trend and anomaly detection.


```python
# Import the PourYa module (adjust the import based on your project structure)
from ouradatahandler import OuraDataHandler

# Define API endpoint, CSV file paths, and the access token.
api_address = "https://api.ouraring.com"
local_data_paths = {
    'daily_sleep': 'data/daily_sleep.csv',
    'sleep': 'data/sleep.csv',
    'daily_activity': 'data/daily_activity.csv'
}
access_token = "YOUR_ACCESS_TOKEN"

# Instantiate the OuraDataHandler class
handler = OuraDataHandler(api_address, local_data_paths, access_token)

# Example 1: Fetch and plot deep sleep duration using CSV data for a specific period
handler.get_deep_sleep_duration(
    source="csv",
    start_date="2024-01-01",
    duration="week",
    caption="Deep Sleep Duration Over the Past Week (CSV Data)"
)

# Example 2: Fetch and plot daily activity data from the API with trend and anomaly detection
handler.get_and_plot_daily_data(
    data_type="daily_activity",
    source="api",
    start_date="2024-02-01",
    duration="month",
    caption="Daily Activity Trends with Anomaly Detection",
    detect_trends=True,
    n_bkps=5,
    detect_anomalies=True,
    anomaly_threshold=2.5
)

```
**Explanation:**

- **Instantiation:**  
The *PourYa* library is instantiated with the API endpoint, local CSV paths, and an access token so the user can effortlessly switch from one data source to another.


- **Deep Sleep Duration Plot:**  
  The `get_deep_sleep_duration` method will plot deep sleep duration for a week (CSV data) by specifying the `duration` parameter.


- **Daily Activity Data Plot:**  
  The method get_and-`get_and_plot_daily_data` retrieves daily activity data from the API and augments the plot with various trend-detection and anomaly-spotting techniques. This is an example showing the library's ability to enhance routine analyses with ease and sophistication.
  
## References

1. Oura Ring. (n.d.). *Oura Ring Official Website*. Retrieved from [https://ouraring.com](https://ouraring.com)
2. pandas documentation. (n.d.). *pandas: Python Data Analysis Library*. Retrieved from [https://pandas.pydata.org](https://pandas.pydata.org)
3. matplotlib documentation. (n.d.). *matplotlib: Python plotting library*. Retrieved from [https://matplotlib.org](https://matplotlib.org)
4. Truong, C., Oudre, L., & Vayatis, N. (2020). *Selective review of offline change point detection methods*. Signal Processing, 167, 107299.

## Acknowledgements

The open-source community is also credited for developing a number of the Python libraries that *PourYa* is making use of-inclusive of pandas, matplotlib, and ruptures. Special thanks also to the team of developers behind the Oura Ring API, which has opened up new possibilities for research into digital health.
