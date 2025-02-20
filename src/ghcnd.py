import argparse
import gzip
import os
from pathlib import Path

import pandas as pd
import requests


class GHCND():
    def __init__(self, datalake_root):
        """
        Represents the ghcnd datalake

        :param datalake_root:
        """

        self.datalake_root = datalake_root
        self.raw_stations_path = self.datalake_root / 'raw' / 'ghcnd-stations.txt'
        self.yearly_files = None

        # load sources
        self.sources = {
            "readme": "https://docs.opendata.aws/noaa-ghcn-pds/readme.html",
            "stations": "http://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-stations.txt",
            "inventory": "http://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-inventory.txt",
            "bucket": "http://noaa-ghcn-pds.s3.amazonaws.com"
        }

    def init_datalake(self, overwrite=False):
        """
        Check for existing Directory structure. Create it if it doesn't exist. only overwrite if overwrite=True
        """


        if not os.path.exists(self.datalake_root):
            os.makedirs(self.datalake_root)
        self._create_sub_directory('raw')
        self._create_sub_directory('raw/daily')
        self._create_sub_directory('clean')
        self._create_sub_directory('clean/daily')
        self._create_sub_directory('curated')
        self._create_sub_directory('metadata')

    def _create_sub_directory(self, relative_path):
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

    def download_daily_data(self, start_year, end_year):
        """
        Download the yearly data inside the data range given. Both start year and end year are inclusive.
        """
        for year in range(start_year, end_year + 1):
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
        stations = pd.read_fwf(self.raw_stations_path,
                               header=None,
                               colspecs=[
                                   (0, 11),
                                   (12, 20),
                                   (21, 30),
                                   (31, 37),
                                   (38, 40),
                                   (41, 71),
                                   (72, 75),
                                   (76, 79),
                                   (80, 85)
                               ]
                               )
        stations.columns = [
            'station_id',
            'latitude',
            'longitude',
            'elevation',
            'state',
            'name',
            'gsn_flag',
            'hcn_crn_flag',
            'wmo_id'
        ]
        stations['station_id'] = stations['station_id'].astype(str)
        stations['latitude'] = stations['latitude'].astype(float)
        stations['longitude'] = stations['longitude'].astype(float)
        stations['elevation'] = stations['elevation'].astype(float)
        stations['name'] = stations['name'].astype(str)
        stations.drop(columns=['state', 'gsn_flag', 'hcn_crn_flag', 'wmo_id'], inplace=True)
        stations.to_parquet(self.datalake_root / 'clean' / 'stations.parquet')

    def clean_daily(self, start_year, end_year):
        """
        Cleans the yearly 'daily' files inside the data range given. Both start year and end year are inclusive.
        :param start_year:
        :param end_year:
        """
        for year in range(start_year, end_year + 1):
            self._clean_daily_file(year)

    def _clean_daily_file(self, year):
        """
        Cleans a single yearly daily file
        :param year:
        """
        daily_dtypes = {
            'station_id': 'str',
            'element': pd.CategoricalDtype(),
            'm_flag': pd.CategoricalDtype(),
            'q_flag': pd.CategoricalDtype(),
            's_flag': pd.CategoricalDtype(),
            'date': str,
            'time': str,
            'value': 'float'
        }
        file = self.datalake_root / 'raw' / 'daily' / f'{year}.csv.gz'
        df = None
        try:
            df = pd.read_csv(file,
                             header=None,
                             names=[
                                 'station_id',
                                 'date',
                                 'element',
                                 'value',
                                 'm_flag',
                                 'q_flag',
                                 's_flag',
                                 'time'
                             ],
                             dtype=daily_dtypes,
                             engine='pyarrow')
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df.drop(columns=['time', 'date'], inplace=True)
            df.to_parquet(self.datalake_root / 'clean' / 'daily' / f'{year}.parquet')
            print(f'SUCCESS: cleaned {file}')
        except gzip.BadGzipFile:
            print(f'ERROR: Bad gzip file {file}')

    def download_metadata(self):
        self._download_file(self.sources['readme'], self.datalake_root / 'metadata' / 'daily.html')


def build_datalake(datalake_root, start_year, end_year, overwrite=False):
    ghcnd = GHCND(Path(datalake_root))

    if not overwrite:
        print("WARNING: Existing dataset detected, set overwrite=True to overwrite. Exiting!")
        return 0

    # Initialize Datalake and download raw data
    ghcnd.init_datalake()
    ghcnd.download_metadata()
    ghcnd.download_stations()
    ghcnd.download_daily_data(start_year, end_year)

    # clean data
    ghcnd.clean_stations()
    ghcnd.clean_daily(start_year, end_year)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process GHCND data.')
    parser.add_argument('datalake_root', type=str, help='Path to the datalake root directory')
    parser.add_argument('start_year', type=int, help='Start year for data download')
    parser.add_argument('end_year', type=int, help='End year for data download')

    args = parser.parse_args()

    # datalake_root = Path('C:/Users/dhruv/IdeaProjects/ghcnd/data')
    # start_year = 2000
    # end_year = 2004
    datalake_root = args.datalake_root
    start_year = args.start_year
    end_year = args.end_year
    # print(datalake_root, start_year, end_year)

    print("Are you sure you want to execute with these arguments?")
    print(f'Path: {datalake_root}')
    print(f'Start year: {start_year}')
    print(f'End year: {end_year}')

    should_continue = input('(y/n): ')
    if should_continue == 'y':
        build_datalake(datalake_root, start_year, end_year)
