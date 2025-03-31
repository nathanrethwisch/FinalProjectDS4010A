import gzip
import os
from pathlib import Path

import pandas as pd
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import requests


class GHCND():
    def __init__(self):
        """
        Represents the ghcnd datalake

        :param datalake_root:
        """
        self.start_year = 1900
        self.end_year = 2025
        self.elements = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN', 'AWND']
        self.datalake_root = Path.home() / 'capstone-data'
        print(self.datalake_root)
        self.raw_stations_path = self.datalake_root / 'raw' / 'ghcnd-stations.txt'
        self.yearly_files = None

        # load sources
        self.sources = {"readme": "https://docs.opendata.aws/noaa-ghcn-pds/readme.html",
            "stations": "http://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-stations.txt",
            "inventory": "http://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-inventory.txt",
            "bucket": "http://noaa-ghcn-pds.s3.amazonaws.com"}

    def init_datalake(self, overwrite=False):
        """
        Check for existing Directory structure. Create it if it doesn't exist. only overwrite if overwrite=True
        """

        if not os.path.exists(self.datalake_root):
            os.makedirs(self.datalake_root)
        self.create_sub_directory('raw')
        self.create_sub_directory('raw/daily')
        self.create_sub_directory('clean')
        self.create_sub_directory('clean/daily')
        self.create_sub_directory('curated')
        self.create_sub_directory('metadata')

    def create_sub_directory(self, relative_path):
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
        Download the yearly data inside the data range given. Both start year and end year are inclusive.
        """
        for year in range(self.start_year, self.end_year + 1):
            file_url = f'{self.sources["bucket"]}/csv.gz/by_year/{year}.csv.gz'
            dest_path = self.datalake_root / 'raw/daily' / f'{year}.csv.gz'
            self._download_file(file_url, dest_path)

    @staticmethod
    def _download_file(file_url, dest_path):
        """
        If file is less than 1GiB then direct download and save to disk.
        If file is larger than 1GiB stream download to disk
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
        Reads the ghcnd-stations fixed-width file and saves it as a parquet
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
        Cleans the yearly 'daily' files inside the data range given. Both start year and end year are inclusive.
        :param start_year:
        :param end_year:
        """
        for year in range(self.start_year, self.end_year + 1):
            print(f'CLEANING {year}.csv.gz')
            self._clean_daily_file(year)

    def _clean_daily_file(self, year):
        """
        Cleans a single yearly daily file
        :param year:
        """
        daily_dtypes = {'station_id': 'str', 'element': pd.CategoricalDtype(), 'm_flag': pd.CategoricalDtype(),
            'q_flag': pd.CategoricalDtype(), 's_flag': pd.CategoricalDtype(), 'date': str, 'time': str,
            'value': 'float'}
        file = self.datalake_root / 'raw' / 'daily' / f'{year}.csv.gz'
        df = None
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
        self._download_file(self.sources['readme'], self.datalake_root / 'metadata' / 'daily.html')

    def create_element_tables(self):
        dataset = ds.dataset(self.datalake_root / 'clean' / 'daily')

        for element in self.elements:
            self.create_sub_directory(f'curated/{element}')
            for year in range(self.start_year, self.end_year + 1):
                print(f'PROCESSING {element}, {year} ')
                filter = (pc.field('element') == element) & (pc.field('year') == year)
                table = dataset.filter(filter).to_table(columns=['station_id', 'year', 'month', 'day', 'value'])
                table = table.rename_columns(['station_id', 'year', 'month', 'day', element])
                pq.write_table(table, self.datalake_root / 'curated' / element / f'{year}.parquet')

    def join_element_tables(self):
        self.create_sub_directory('curated/combined')

        for year in range(self.start_year, self.end_year + 1):
            table = pq.read_table(self.datalake_root / 'curated' / self.elements[0] / f'{year}.parquet')
            for i in range(1, len(self.elements)):
                t2 = pq.read_table(self.datalake_root / 'curated' / self.elements[i] / f'{year}.parquet')
                table = table.join(t2, keys=['station_id', 'year', 'month', 'day'], join_type='full outer')

            pq.write_table(table, self.datalake_root / 'curated' / 'combined' / f'{year}.parquet')
