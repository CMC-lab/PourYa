---
title: "PourYa: A unified library for handling and visualizing Oura ring data"
tags:
  - Python
  - Digital health
date: "2025-02-14"

authors:
  - name: "Ali Mohammadi"
    affiliation: 1
    orcid: 0009-0005-3460-7796
  - name: "Saeed Niksaz"
    affiliation: 2
    orcid: 0009-0003-4025-3459
  - name: "Shervin Safavi"
    affiliation: [3,4]
    orcid: 0000-0002-2868-530X

affiliations:
  - index: 1
    name: "Department of Computer Engineering, University of Tehran"
  - index: 2
    name: "Linnaeus University, Kalmar, Sweden"
  - index: 3
    name: "Computational Neuroscience, Department of Child and Adolescent Psychiatry, Faculty of Medicine, Technische Universität Dresden, Dresden 01307, Germany"
  - index: 4
    name: "Department of Computational Neuroscience, Max Planck Institute for Biological Cybernetics, Tübingen 72076, Germany"

bibliography: paper.bib
---

## Summary

*PourYa* is an open-source Python for basic analysis of health data resulted from Oura smart rings [@OuraRing]. 
*PourYa* (Py + Oura) provides a unified interface to API-based and CSV-based data. *PourYa* makes it easier for researchers and practitioners to explore a variety of health metrics, from sleep patterns to daily activity to heart rate variation. The core function of this package also contains some advanced analytics like trend detection via change point analysis and anomaly detection [@truong2020selective], thus making it suitable for digital healthcare research and personal wellness analytics. Furthermore, given that *PourYa* is developed based on principles of open software, it can be easily extended with new and more sophisticated data analysis methods.

## Statement of need

*PourYa* is designed to be used by digital health researchers, neuroscientisit, psychologist, machine learners, and by non-scientist
users of Oura ring (e.g., for monitoring their health data). 
Oura ring has already been used in a number of scientific publications (e.g., see,  [@cao2022accuracy; @svensson2024validity]). 
Furthermore, digital phenotyping is rapidly growing in digital health and computational psychiatry [@ressler2021big], and can further be combined with measuring cognitive states [@denis2022sleep; @donegan2023using; @gillan2016taking; @kelley2022using; @safavi2022multistability; @safavi2024decision].

*PourYa* can smoothen the workflows for handling data from Oura rings.
Current workflows for handling data from Oura rings involve custom scripts and manual integration of multiple libraries, which potentialy increase the risk of errors and reducing reproducibility.
Furthermore, two existing approaches to retrieving the data (Oura API and CSV exports, which codes for the latter is more scarce) require different collection of codes to handle the data, which is now integrated in *PourYa*.
Thus, *PourYa* provide an integrated, open-source solution that offers a configurable toolkit for the entire data process — from fetching and processing data to trend analysis and anomaly detection — using established Python libraries.

## Functionality and implementation

*PourYa* is an open-source Python library meant to facilitate Oura ring data processing and visualization. The entire workflow from data acquisition to final visualization is wrapped around the class called `OuraDataHandler`.


### Core functionalities


- **Data acquisition:**
*PourYa* is designed to obtain and manage data from both the Oura API and locally stored CSV files. Merging the data acquisition through both channel (Oura API and locally stored CSV files) was intentional to make the analysis pipeline data-source agnostic.

   - **Fetching Data from the Oura API**
*PourYa* can fetch real-time data directly from the Oura API using the `fetch_data_from_api` method. Users can specify the data type and date range, and the library retrieves relevant records from the API.

   - **Loading Data from Local CSV Files**
Previously saved data can be loaded using the `load_data_from_csv` method. This function allows users to filter stored data based on a specified date range. This allow the CSV files to be analyzed similarly as the one acquired by the API.

  - **Saving Data to CSV Format**
User can also store retrieved or processed data on their computer into CSV files using *PourYa*. This is made so via the `save_to_csv` method, which allows saving information to a CSV file on the disk for future access or integration with other applications. Choice of CSV format is simply due to compatibility with a wide range of packages (e.g., `pandas`), and human readability.

  - **Examples of API Data Retrieval**
    To improve accessibility and clarity, we demonstrate how *PourYa* fetches data from the Oura API:
    - Fetching Data from the API
      The retrieval process from the API starts with the user issuing some simple method calls:
    ```python
    handler = OuraDataHandler(api_address, local_data_paths, access_token)
    
    # Fetch daily activity data
    daily_activity_df = handler.fetch_data_from_api(
        data_type="daily_activity",
        start_date="2024-02-01",
        duration="month",
        save_file=True,
        filename="daily_activity_february.csv"
    )
    ```
    - Internally, the method sets up authenticated HTTP requests:
    ```python
    url = f'{self.api_address}/v2/usercollection/{data_type}'
    headers = {'Authorization': f'Bearer {self.access_token}'}
    params = {'start_date': '2024-01-01', 'end_date': '2024-02-01'}
    response = requests.get(url, headers=headers, params=params, timeout=10)
    ```

    - The responses from the API are converted into pandas DataFrames:

    ```python
    response_json = response.json().get('data', [])
    df = pd.DataFrame.from_dict(response_json, orient='columns')
    ```
- **Date handling:**
  A specific method, `_convert_date`, allows the user to manipulate specific periods (i.e., days, weeks, months, or years) for generating queries to retrieve data over a rolling time frame.
  
- **Visualization:**
  Various plot methods are made available for different analytical purposes:
  - `plot_data`, with custom line plots, automatically attempts detection of trend (using the *ruptures* package; also, see next item) and anomaly highlighting (which can be easily expanded by the community);
  - `plot_sleep_phases` visually plots various sleep stages in 5-minute intervals (which is the resolution imposed Oura ring), converting the phase numbers into a more easily identifiable colored graph;
  - `plot_bedtime` and `plot_heart_rate` are aimed at understanding patterns related to going to bed and heart rate, respectively.

- **Trend and anomaly detection:**
  Using *ruptures*, *PourYa*  marks change points for time series data that represent significant shifts in the metrics. Z-scores through rolling statistics have been utilized to flag potential outliers that are likely anomalies. This can be further extended, for instance, by incorporating recent developments in anomaly detection's [@chen2024pyod2pythonlibrary].


### Implementation details

- **Class-based structure:**
  The functional structure of this class, known as the **OuraDataHandler** class, allows extensibility and integration in data processing pipelines. Its constructor takes arguments in the form of API credentials and paths to local CSV.


- **Robust data handling:**
  Date filtering is done based on the date ranges that the user supplies, with error-handling capabilities that allow missing or incorrect parameters. This ensures that only valid data makes it through for filtering and visualization. 


- **Integration with established libraries:**  
  By building on top of widely used Python libraries—such as `pandas` [@pandas2020] for data manipulation, `matplotlib` [@hunter2007matplotlib] for plotting, and `ruptures` [@truong2020selective] for change point detection

- **Modular and extensible design:**
*PourYa*, with distinct methods to do each job, is done in order to emphasize on readability and maintainability of code while allowing other contributors to extend functionalities by a minimum rewriting effort (for example, by adding new metrics or visualization techniques).

## Example usage

Below is an example of how to call *PourYa* to retrieve sleep data from a local CSV file and visualize it, as well as do a similar for daily activity data from the API, with trend and anomaly detection.


```python
# Import the *PourYa* module (adjust the import based on your project structure)
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

![Deep Sleep Duration](figures/deep_sleep_plot.pdf){#fig:deep-sleep width=90%}

![Daily Activity Trends](figures/daily_activity_plot.pdf){#fig:daily-activity width=90%}


**Explanation:**

- **Instantiation:**
The *PourYa* library is instantiated with the API endpoint, local CSV paths, and an access token so the user can easily switch from one data source to another.


- **Deep sleep duration plot:**
  The `get_deep_sleep_duration` method will plot deep sleep duration for a week (CSV data) by specifying the `duration` parameter.


- **Daily activity data plot:**  
  The method get_and-`get_and_plot_daily_data` retrieves daily activity data from the API and augments the plot with various trend-detection and anomaly-spotting techniques. This is an example showing the library's ability to enhance routine analyses with ease and sophistication.
  

## Acknowledgments

The open-source community is also credited for developing a number of the Python libraries that *PourYa* is making use of-inclusive of pandas, matplotlib, and ruptures. 
SS acknowledges the add-on fellowship from the Joachim Herz Foundation.

## References

