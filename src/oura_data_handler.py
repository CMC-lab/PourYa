import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import timedelta, datetime
from IPython.display import display, Markdown
import ruptures as rpt


class OuraDataHandler:
    """
    A library for handling Oura Ring data: fetching from API, loading from CSV, and visualising metrics.
    """

    def __init__(self, api_address: str, local_data_paths: dict, access_token: str):
        """
        Initialise the OuraDataHandler with API details and data paths.

        :param api_address: API base address for data requests.
        :param local_data_paths: Dictionary mapping data types to file paths for CSVs.
        :param access_token: Personal access token for the Oura API.
        """
        self.api_address = api_address
        self.local_data_paths = local_data_paths
        self.access_token = access_token

    def _convert_date(self, input_date: str, period: str = None) -> str:
        """
        Convert a given date into a new date adjusted by a specified period.

        :param input_date: Date in 'YYYY-MM-DD' format.
        :param period: One of 'day', 'week', 'month', or 'year'. Adjusts input date accordingly.
        :return: Adjusted date in 'YYYY-MM-DD' format.
        """
        date_format = '%Y-%m-%d'
        parsed_date = datetime.strptime(input_date, date_format).date()
        if period == "week":
            adjusted_date = parsed_date - timedelta(days=7)
        elif period == "month":
            adjusted_date = parsed_date - timedelta(days=30)
        elif period == "year":
            adjusted_date = parsed_date - timedelta(days=365)
        elif period == "day":
            adjusted_date = parsed_date + timedelta(days=1)
        else:
            adjusted_date = parsed_date
        return adjusted_date.strftime(date_format)

    def fetch_data_from_api(self, data_type: str, start_date: str, end_date: str = None, duration: str = None, save_file: bool = False, filename: str = None) -> pd.DataFrame:
        """
        Fetch data from the Oura API for a specific type and date range.

        :param data_type: Type of data to fetch (e.g., 'sleep', 'heartrate').
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format (optional).
        :param duration: Duration period to adjust the start date (optional).
        :return: Data as a pandas DataFrame.
        """
        if not self.access_token:
            print("Invalid token!")
            return pd.DataFrame()

        # Valid data types for Oura API
        valid_data_types = [
            'sleep', 'daily_sleep', 'daily_activity', 'daily_readiness', 'daily_spo2', 
            'heartrate', 'daily_stress'
        ]
        if data_type not in valid_data_types:
            print("Invalid data type!")
            return pd.DataFrame()

        print(f"Requesting {data_type} data... ", end='')

        # Build request parameters
        if end_date is None:
            new_start_day = self._convert_date(start_date, duration)
            end_date = start_date
            if data_type != "heartrate":
                params = {'start_date': f'{new_start_day}', 'end_date': f'{end_date}'}
            else:
                new_end_day = self._convert_date(start_date, "day")
                params = {'start_datetime': f'{new_start_day}', 'end_datetime': f'{new_end_day}'}
        else:
            params = {'start_date': f'{start_date}', 'end_date': f'{end_date}'}
            
        # Make the API request
        url = f'{self.api_address}/v2/usercollection/{data_type}'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response_json = response.json().get('data', [])

        if not response_json:
            print('No data received.')
            return pd.DataFrame()

        print('done!')
        df = pd.DataFrame.from_dict(response_json, orient='columns')
        if save_file:
            if df.empty:
                print("No data available to save.")
                return
            df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
        return df
    def save_to_csv(self, df: pd.DataFrame, filename: str):
        """
        Save the given DataFrame to a CSV file.
    
        :param df: Data to be saved (Pandas DataFrame).
        :param filename: Name of the CSV file.
        """
        if df.empty:
            print("No data available to save.")
            return
    
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    def load_data_from_csv(self, data_type: str, start_date: str, end_date: str = None, duration: str = None) -> pd.DataFrame:
        """
        Load data from a local CSV file for a specific type and date range.

        :param data_type: Type of data to load (e.g., 'daily_sleep').
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format (optional).
        :param duration: Duration period to adjust the start date (optional).
        :return: Data as a pandas DataFrame.
        """
        file_path = self.local_data_paths.get(data_type)
        if not file_path:
            print("Invalid data type for CSV!")
            return pd.DataFrame()

        df = pd.read_csv(file_path)
        if end_date is None:
            target_date = self._convert_date(start_date, duration)
            return df.loc[(df['day'] >= target_date) & (df['day'] <= start_date)]
        else:
            return df.loc[(df['day'] >= start_date) & (df['day'] <= end_date)]

    def plot_data(self, df: pd.DataFrame, column: str = 'score', y_label: str = 'Score', title: str = 'Data Plot', 
                  caption: str = '', x_labels: list = None, column2: str = None, detect_trends: bool = False, 
                  n_bkps: int = 0, detect_anomalies: bool = False, anomaly_threshold: float = 2.0):
        """
        Plot the data with options for trends and anomalies.

        :param df: DataFrame containing the data to plot.
        :param column: Column to plot on the Y-axis.
        :param y_label: Label for the Y-axis.
        :param title: Title of the plot.
        :param caption: Caption for the plot.
        :param x_labels: Custom labels for the X-axis.
        :param column2: Optional secondary column to plot.
        :param detect_trends: Whether to detect and plot trends.
        :param n_bkps: Number of breakpoints to detect for trends.
        :param detect_anomalies: Whether to detect and highlight anomalies.
        :param anomaly_threshold: Z-score threshold for anomalies.
        """
        if df.empty:
            print("No data to plot.")
            return

        # Plot setup
        plt.rcParams.update({'font.size': 14})
        fig, ax = plt.subplots(figsize=(18, 6))
        mean_value = df[column].mean()

        # Main plot
        ax.plot(df['day'], df[column], color='black', linewidth=2, label=f'Daily {column}')
        ax.axhline(mean_value, label=f'Mean {column} = {mean_value:1.2f}', ls='dashed', color='blue', linewidth=2)

        # Optional second column plot
        if column2:
            mean_value2 = df[column2].mean()
            ax.plot(df['day'], df[column2], color='red', linewidth=2, label=f'Daily {column2}')
            ax.axhline(mean_value2, label=f'Mean {column2} = {mean_value2:1.2f}', ls='dashed', color='green', linewidth=2)

        # Trend detection
        if detect_trends:
            signal = df[column].dropna().values
            algo = rpt.Pelt(model="l2").fit(signal)
            change_points = algo.predict(pen=np.log(len(signal)))
            for cp in change_points[:-1]:
                change_date = df['day'].iloc[cp]
                ax.axvline(x=change_date, color='red', linestyle='--', label=f'Change Point: {change_date}')

        # Anomaly detection
        if detect_anomalies:
            rolling_mean = df[column].rolling(window=7, min_periods=1).mean()
            rolling_std = df[column].rolling(window=7, min_periods=1).std()
            z_scores = (df[column] - rolling_mean) / rolling_std
            anomalies = df.loc[abs(z_scores) > anomaly_threshold]
            if not anomalies.empty:
                ax.scatter(anomalies['day'], anomalies[column], color='red', label='Anomalies', zorder=5)

        # Plot aesthetics
        ax.tick_params(axis='x', rotation=45)
        ax.set_xlabel('Day', fontsize=14)
        ax.set_ylabel(y_label, fontsize=14)
        ax.set_title(title, fontsize=16)
        ax.legend(fontsize=12)
        plt.show()

        if caption:
            display(Markdown(f"**Figure:** {caption}"))

    def get_deep_sleep_duration(self, source: str, start_date: str, end_date: str = None, duration: str = None, caption: str = ''):
        """
        Get and plot the deep sleep duration over a specified period.

        :param source: Data source, either 'csv' or 'api'.
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format (optional).
        :param duration: Duration period to adjust the date range (optional).
        :param caption: Caption for the plot (optional).
        """
        if source == "csv":
            df = self.load_data_from_csv('daily_sleep', start_date=start_date, end_date=end_date, duration=duration)
        elif source == "api":
            df = self.fetch_data_from_api('daily_sleep', start_date, end_date=end_date, duration=duration)
            if not df.empty:
                df = pd.concat([df.drop(columns=['contributors']), pd.json_normalize(df['contributors'])], axis=1)
                df.rename(columns={'deep_sleep': 'contributors_deep_sleep'}, inplace=True)
        else:
            print("Invalid data source!")
            return

        if not df.empty:
            self.plot_data(df, column='contributors_deep_sleep', y_label='Deep Sleep Duration', 
                           title='Deep Sleep Duration Over Time', caption=caption)
        else:
            print("No data available for plotting.")
            
    def get_and_plot_daily_data(self, data_type: str, source: str, start_date: str, end_date: str = None, 
                                duration: str = None, caption: str = '', peacewisedDays: int = 1, 
                                detect_trends: bool = False, n_bkps: int = 10, detect_anomalies: bool = False, 
                                anomaly_threshold: float = 2.0):
        """
        Fetch and plot daily data for specified metrics.

        :param data_type: Type of data to fetch and plot (e.g., 'daily_activity').
        :param source: Data source, either 'csv' or 'api'.
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format (optional).
        :param duration: Duration period to adjust the date range (optional).
        :param caption: Caption for the plot (optional).
        :param peacewisedDays: Number of days to aggregate for the plot.
        :param detect_trends: Whether to detect and plot trends.
        :param n_bkps: Number of breakpoints to detect for trends.
        :param detect_anomalies: Whether to detect and highlight anomalies.
        :param anomaly_threshold: Z-score threshold for anomalies.
        """
        # Load data based on the source
        if source == 'csv':
            df = self.load_data_from_csv(data_type, start_date=start_date, end_date=end_date, duration=duration)
        elif source == 'api':
            df = self.fetch_data_from_api(data_type, start_date=start_date, end_date=end_date, duration=duration)
        else:
            print("Invalid data source!")
            return

        if df.empty:
            print("No data available to plot.")
            return
        
        # Plot data with appropriate parameters
        if peacewisedDays == 1:
            if data_type == 'daily_spo2':
                if source == 'api':
                    df = df.dropna(subset=['spo2_percentage'])
                    df['spo2_percentage'] = df['spo2_percentage'].apply(lambda x: x['average'])
                self.plot_data(
                    df=df,
                    column='spo2_percentage',
                    y_label=f'{data_type.replace("_", " ").capitalize()} Score',
                    title=f'Daily {data_type.replace("_", " ").capitalize()}',
                    caption=caption,
                    detect_trends=detect_trends,
                    n_bkps=n_bkps,
                    detect_anomalies=detect_anomalies,
                    anomaly_threshold=anomaly_threshold
                )
            else:
                self.plot_data(
                    df=df,
                    column='score',
                    y_label=f'{data_type.replace("_", " ").capitalize()} Score',
                    title=f'Daily {data_type.replace("_", " ").capitalize()}',
                    caption=caption,
                    detect_trends=detect_trends,
                    n_bkps=n_bkps,
                    detect_anomalies=detect_anomalies,
                    anomaly_threshold=anomaly_threshold
                )
        else:
            if data_type == 'daily_spo2':
                if source == 'api':
                    df = df.dropna(subset=['spo2_percentage'])
                    df['spo2_percentage'] = df['spo2_percentage'].apply(lambda x: x['average'])
                column = 'spo2_percentage'
            else:
                column = 'score'
            df['day'] = pd.to_datetime(df['day'])
            df = df.set_index('day').sort_index()
            df_resampled = df[column].resample(f'{peacewisedDays}D').mean()
            period_labels = [
                f"{(date).strftime('%Y-%m-%d')} to {(date + pd.Timedelta(days=peacewisedDays-1)).strftime('%Y-%m-%d')}"
                for date in df_resampled.index
            ]
            if df.empty:
                print("No data to plot.")
                return
            plt.rcParams.update({'font.size': 14})

            mean_value = df[column].mean()
            fig, ax = plt.subplots(figsize=(18, 6))
            y_label=f'{data_type.replace("_", " ").capitalize()} {column}'
            title=f'Daily {data_type.replace("_", " ").capitalize()}'
            ax.plot(df_resampled.index, df_resampled.values, color='black', linewidth=2, label=f'Daily {y_label}')
            ax.axhline(mean_value, label=f'Mean score = {mean_value:1.2f}', ls='dashed', color='blue', linewidth=2)
            if detect_trends:
                signal = df[column].dropna().values
                algo = rpt.Pelt(model="rbf").fit(signal)
                change_points = algo.predict(pen=np.log(len(signal))) 
                for cp in change_points[:-1]:  
                    change_date = df['day'].iloc[cp]
                    plt.axvline(x=change_date, color='red', linestyle='--', label=f'Change Point: {change_date}')
            anomalies = []
            if detect_anomalies:
                rolling_mean = df[column].rolling(window=7, min_periods=1).mean()
                rolling_std = df[column].rolling(window=7, min_periods=1).std()
                z_scores = (df[column] - rolling_mean) / rolling_std
                anomalies = df.loc[abs(z_scores) > anomaly_threshold]
                if detect_anomalies and not anomalies.empty:
                    plt.scatter(anomalies['day'], anomalies[column], color='red', label='Anomalies', zorder=5)
            ax.tick_params(axis='x', rotation=45)
            plt.xticks(df_resampled.index, period_labels, rotation=45, ha='right')
            ax.set_xlabel('Day', fontsize=14)
            ax.set_ylabel(y_label, fontsize=14)
            ax.set_title(title, fontsize=16)
            ax.legend(fontsize=12)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(True)
            ax.spines['bottom'].set_visible(True)
            plt.show()
            if caption != "":
                display(Markdown(f"**Figure:** {caption}"))
            else:
                print("out of range of peacewised Days")
            

    def plot_sleep_phases(self, source: str, date: str, caption: str = ''):
        """
        Plot the sleep phases for a specified date.

        :param source: Data source, either 'csv' or 'api'.
        :param date: Date in 'YYYY-MM-DD' format for which to plot the sleep phases.
        :param caption: Caption for the plot (optional).
        """
        end_date = self._convert_date(date, period="day")
        if source == "csv":
            df = self.load_data_from_csv('sleep', start_date=date, end_date=end_date)
        elif source == "api":
            df = self.fetch_data_from_api('sleep', start_date=date, end_date=end_date)
        else:
            print("Invalid data source!")
            return

        if df.empty:
            print("No data available for plotting.")
            return

        sleep_phases = df.loc[df['day'] == date, 'sleep_phase_5_min'].values[0]
        phase_values = [float(x) for x in sleep_phases]
        start_time = datetime.fromisoformat(df['bedtime_start'].values[0])
        step_interval = timedelta(minutes=5)
        time_labels = [(start_time + i * step_interval).strftime("%H:%M") for i in range(len(phase_values))]

        fig, ax = plt.subplots(figsize=(18, 6))
        colors = {4: 'red', 3: 'blue', 2: 'green', 1: 'purple'}
        line_thickness = 10

        # Draw sleep phases
        for i in range(len(phase_values) - 1):
            ax.hlines(y=phase_values[i], xmin=i, xmax=i+1, color=colors.get(int(phase_values[i]), 'black'), linewidth=line_thickness)

        ax.set_xticks(range(len(time_labels)))
        ax.set_xticklabels(time_labels, rotation=45, fontsize=10)
        ax.set_yticks(list(colors.keys()))
        ax.set_yticklabels(['Awake', 'Light Sleep', 'Deep Sleep', 'REM'], fontsize=12)
        ax.set_xlabel('Time (5-minute intervals)', fontsize=16)
        ax.set_ylabel('Sleep Phase', fontsize=16)
        ax.set_title(f'Sleep Phases on {date}', fontsize=18)
        plt.show()

        if caption:
            display(Markdown(f"**Figure:** {caption}"))

    def plot_bedtime(self, data_type: str, source: str, start_date: str, end_date: str = None, duration: str = None, caption: str = ''):
        """
        Plot bedtime start or end times over a specified period.

        :param data_type: Either 'start' for bedtime start or 'end' for bedtime end.
        :param source: Data source, either 'csv' or 'api'.
        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format (optional).
        :param duration: Duration period to adjust the date range (optional).
        :param caption: Caption for the plot (optional).
        """
        if source == "csv":
            df = self.load_data_from_csv('sleep', start_date=start_date, end_date=end_date, duration=duration)
        elif source == "api":
            df = self.fetch_data_from_api('sleep', start_date, end_date=end_date, duration=duration)
        else:
            print("Invalid data source!")
            return

        if df.empty:
            print("No data available for plotting.")
            return

        if data_type == "start":
            df['bedtime'] = pd.to_datetime(df['bedtime_start'])
            title = 'Bedtime Start'
            label = 'Start Time'
            line_color = 'blue'
        elif data_type == "end":
            df['bedtime'] = pd.to_datetime(df['bedtime_end'])
            title = 'Bedtime End'
            label = 'End Time'
            line_color = 'red'
        else:
            print("Invalid data type!")
            return

        df['bedtime_time'] = df['bedtime'].dt.hour + df['bedtime'].dt.minute / 60

        fig, ax = plt.subplots(figsize=(18, 6))
        ax.stem(df['day'], df['bedtime_time'], linefmt=line_color, markerfmt='o', basefmt=" ", label=label)
        ax.set_title(title, fontsize=16)
        ax.set_xlabel('Day', fontsize=14)
        ax.set_ylabel('Time (Hours)', fontsize=14)
        ax.legend(fontsize=12)
        plt.show()

        if caption:
            display(Markdown(f"**Figure:** {caption}"))

    def plot_heart_rate(self, date: str, source: str = "both", caption: str = "Daily Heart Rate"):
        """
        Plot heart rate data for a specified date.

        :param date: Date in 'YYYY-MM-DD' format for the heart rate plot.
        :param source: Data source to filter, either 'rest', 'awake', or 'both'.
        :param caption: Caption for the plot (optional).
        """
        df = self.fetch_data_from_api("heartrate", start_date=date)

        if df.empty:
            print("No data available for plotting.")
            return

        if source == "rest":
            df = df[df['source'] == "rest"]
        elif source == "awake":
            df = df[df['source'] == "awake"]

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        mean_value = df['bpm'].mean()

        plt.figure(figsize=(18, 6))
        plt.plot(df['hour'] + df['minute'] / 60, df['bpm'], color='black', linewidth=2, label='Heart Rate')
        plt.axhline(mean_value, color='blue', linestyle='--', linewidth=2, label=f'Mean Heart Rate = {mean_value:.2f}')
        plt.xlabel('Time (Hours)', fontsize=14)
        plt.ylabel('Heart Rate (BPM)', fontsize=14)
        plt.title('Heart Rate Over Time', fontsize=16)
        plt.legend(fontsize=12)
        plt.show()

        if caption:
            display(Markdown(f"**Figure:** {caption}"))
