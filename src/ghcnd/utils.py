import gzip
import os
import shutil
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import requests


class GHCND:
    def __init__(self):
        """
        Represents the GHCND dataset, provides functions for dataset aquisition, processing, and querying.
        """
        self.start_year = 1900
        self.end_year = 2025
        self.elements = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN', 'AWND']  # Measurement elements to keep in final tables
        self.datalake_root = Path.home() / 'capstone-ghcnd'
        self.raw_stations_path = self.datalake_root / 'raw' / 'ghcnd-stations.txt'
        self.yearly_files = None

        # load sources
        self.sources = {"readme": "https://docs.opendata.aws/noaa-ghcn-pds/readme.html",
                        "stations": "https://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-stations.txt",
                        "inventory": "https://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-inventory.txt",
                        "bucket": "https://noaa-ghcn-pds.s3.amazonaws.com"}

    def init_datalake(self):
        """
        Check for existing Directory structure. Create it if it doesn't exist. only overwrite if overwrite=True
        """
        print(f"Initializing GHCND dataset at {self.datalake_root}")

        if not os.path.exists(self.datalake_root):
            os.makedirs(self.datalake_root)
        self.create_sub_directory('raw')
        self.create_sub_directory('raw/daily')
        self.create_sub_directory('clean')
        self.create_sub_directory('clean/daily')
        self.create_sub_directory('curated')
        self.create_sub_directory('metadata')

    def create_sub_directory(self, relative_path):
        """
        Creates a directory using paths relative to the datalake root
        :param relative_path: 
        """
        path = self.datalake_root / relative_path
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'{relative_path} folder created')
        else:
            print(f'{relative_path} folder already exists')

    def download_stations(self):
        """
        Download the raw station data
        """
        self._download_file(self.sources['stations'], self.raw_stations_path)

    def download_daily_data(self):
        """
        Download the yearly data inside the year range. Both start year and end year are inclusive.
        """
        for year in range(self.start_year, self.end_year + 1):
            file_url = f'{self.sources["bucket"]}/csv.gz/by_year/{year}.csv.gz'
            dest_path = self.datalake_root / 'raw/daily' / f'{year}.csv.gz'
            self._download_file(file_url, dest_path)

    @staticmethod
    def _download_file(file_url, dest_path):
        """
        Downloads a file from a url to a filesystem path.
        If file is less than 1GiB then direct download and save to disk.
        If file is larger than 1GiB stream download to disk.
        """
        print(f'Downloading {file_url}')
        response = requests.head(file_url)
        file_size = int(response.headers.get('content-length', 0))
        one_gib = 1 * 1024 * 1024 * 1024

        if file_size < one_gib:
            response = requests.get(file_url)
            with open(dest_path, 'wb') as file:
                file.write(response.content)
        else:
            response = requests.get(file_url, stream=True)
            with open(dest_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

    def clean_stations(self):
        """
        Reads the ghcnd-stations fixed-width file, sets datatypes, and saves it as a parquet file.
        """
        stations = pd.read_fwf(self.raw_stations_path, header=None,
                               colspecs=[(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71), (72, 75), (76, 79),
                                         (80, 85)])
        stations.columns = ['station_id', 'latitude', 'longitude', 'elevation', 'state', 'name', 'gsn_flag',
                            'hcn_crn_flag', 'wmo_id']
        stations['station_id'] = stations['station_id'].astype(str)
        stations['latitude'] = stations['latitude'].astype(float)
        stations['longitude'] = stations['longitude'].astype(float)
        stations['elevation'] = stations['elevation'].astype(float)
        stations['name'] = stations['name'].astype(str)
        stations.drop(columns=['state', 'gsn_flag', 'hcn_crn_flag', 'wmo_id'], inplace=True)

        stations.to_parquet(self.datalake_root / 'clean' / 'stations.parquet')

    def clean_daily(self):
        """
        Converts the yearly csv.gz files to parquet files.
        """
        for year in range(self.start_year, self.end_year + 1):
            print(f'CLEANING {year}.csv.gz')
            self._clean_daily_file(year)

    def _clean_daily_file(self, year):
        """
        Converts a single yearly csv.gz file. Sets datatypes, drops unwanted columns, and saves it as a parquet file.
        :param year:
        """
        daily_dtypes = {'station_id': 'str', 'element': pd.CategoricalDtype(), 'm_flag': pd.CategoricalDtype(),
                        'q_flag': pd.CategoricalDtype(), 's_flag': pd.CategoricalDtype(), 'date': str, 'time': str,
                        'value': 'float'}
        file = self.datalake_root / 'raw' / 'daily' / f'{year}.csv.gz'
        try:
            df = pd.read_csv(file, header=None,
                             names=['station_id', 'date', 'element', 'value', 'm_flag', 'q_flag', 's_flag', 'time'],
                             dtype=daily_dtypes, engine='pyarrow')
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df.drop(columns=['time', 'date', 'm_flag', 'q_flag', 's_flag'], inplace=True)
            df.to_parquet(self.datalake_root / 'clean' / 'daily' / f'{year}.parquet')
            print(f'SUCCESS: cleaned {file}')
        except gzip.BadGzipFile:
            print(f'ERROR: Bad gzip file {file}')

    def download_metadata(self):
        """
        Downloads the ghncd metadata html file
        """
        self._download_file(self.sources['readme'], self.datalake_root / 'metadata' / 'daily.html')

    def create_element_tables(self):
        """
        Separates records into tables where each table includes only a single element type as a column instead of rows.
        Also filters all records, keeping only records originating from weather stations in US, CA, and MX (FIPS COUNTRY CODES).
        """
        dataset = ds.dataset(self.datalake_root / 'clean' / 'daily')
        stations_na = pq.read_table(self.datalake_root / 'curated' / 'stations.parquet')
        stations_na_ids = stations_na['station_id']

        for element in self.elements:
            self.create_sub_directory(f'curated/{element}')

            for year in range(self.start_year, self.end_year + 1):  # Process a single year at a time
                print(f'PROCESSING {element}, {year} ')

                query = ((pc.is_in(pc.field('station_id'), value_set=stations_na_ids))  # Filter for NA stations
                         & (pc.field('element') == element)  # Filter for desired element
                         & (pc.field('year') == year))

                table = dataset.filter(query).to_table(columns=['station_id', 'year', 'month', 'day', 'value'])
                table = table.rename_columns(['station_id', 'year', 'month', 'day', element])

                pq.write_table(table, self.datalake_root / 'curated' / element / f'{year}.parquet')

    def join_element_tables(self):
        """
        Joins the element tables generated by ghcnd.create_element_tables() into a single table. 
        """
        self.create_sub_directory('curated/combined')

        for year in range(self.start_year, self.end_year + 1):  # Process a single year at a time
            print(f'JOINING ELEMENTS: {year} ')

            table = pq.read_table(self.datalake_root / 'curated' / self.elements[
                0] / f'{year}.parquet')  # Read the first element for the given year
            for i in range(1,
                           len(self.elements)):  # Iteratively join rest of the given year's elements to the first element's table
                t2 = pq.read_table(self.datalake_root / 'curated' / self.elements[i] / f'{year}.parquet')
                table = table.join(t2, keys=['station_id', 'year', 'month', 'day'],  # "Primary key" is a tuple of these
                    join_type='full outer')  # Return all records(some station/date combinations may have N/A values for element columns) # TODO CHECK THIS JOIN LOGIC

            pq.write_table(table, self.datalake_root / 'curated' / 'combined' / f'{year}.parquet')

    def join_stations_elements(self):
        """
        Join the stations with the combined element tables. This produces the final dataset in ghcnd.datalake_root/curated/final/
        """
        self.create_sub_directory('curated/final')
        stations = pq.read_table(self.datalake_root / 'curated' / 'stations.parquet')
        for year in range(self.start_year, self.end_year + 1):
            print(f'JOINING: STATIONS & {year}')

            table = pq.read_table(self.datalake_root / 'curated' / 'combined' / f'{year}.parquet')

            joined = stations.join(table, keys='station_id',
                                   join_type='inner')  # inner join means that stations without records will be dropped. #TODO CHECK THIS JOIN LOGIC
            pq.write_table(joined, self.datalake_root / 'curated' / 'final' / f'{year}.parquet')

    def filter_na_stations(self):
        """
        Filter stations retaining only US, CA, MX stations.
        """
        stations = pq.read_table(self.datalake_root / 'clean' / 'stations.parquet')

        us_stations = stations.filter(pc.starts_with(stations['station_id'], 'US'))
        ca_stations = stations.filter(pc.starts_with(stations['station_id'], 'CA'))
        mx_stations = stations.filter(pc.starts_with(stations['station_id'], 'MX'))

        # Concatenate the filtered tables
        stations = pa.concat_tables([us_stations, ca_stations, mx_stations])
        pq.write_table(stations, self.datalake_root / 'curated' / 'stations.parquet')

    def query(self, query_expression: ds.Expression, columns: list[str] = None):
        """
        A helper function which queries the GHCND dataset. Use this to generate pandas dataframes with the desired columns and records 
        :param filter: A pyarrow filter(https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Expression.html#pyarrow.dataset.Expression)
        :param columns: A list of column names
        """
        dataset = ds.dataset(self.datalake_root / 'curated' / 'final')
        df = dataset.filter(query_expression).to_table(columns=columns).to_pandas()

        return df

    def clean_data(self):
        """
        Removes nulls, Converts units...
        """
        pass

    def clean_disk(self, delete_raw_data=False):
        """
        Clean up intermediate tables. Optionally delete the raw data(NOT RECOMMENDED!).
        """
        paths = ['clean/', 'curated/combined']
        for element in self.elements:
            paths.append(f'curated/{element}')

        for path in paths:
            path = self.datalake_root / path
            print(f'REMOVING: {path}')
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"File {path} DELETED SUCCESSFULLY.")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"DIRECTORY {path} DELETED SUCCESSFULLY.")

        if delete_raw_data:
            if os.path.exists(self.datalake_root / 'raw'):
                print(f'REMOVING: {self.datalake_root / "raw"}')
                shutil.rmtree(self.datalake_root / 'raw')
