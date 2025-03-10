import os
from pathlib import Path
import pandas as pd

import requests

paths = {"ghcnd_raw_stations": "raw/ghcnd/stations.txt", "ghcnd_raw_daily": "raw/ghcnd/daily/",
    "ghcnd_clean_stations": "clean/ghcnd/stations.parquet", "ghcnd_clean_daily": "clean/ghcnd/daily/"}
ghcnd_sources = {"readme": "https://docs.opendata.aws/noaa-ghcn-pds/readme.html",
                 "stations": "https://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-stations.txt",
                 "inventory": "https://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-inventory.txt",
                 "bucket": "https://noaa-ghcn-pds.s3.amazonaws.com"}
years = (2000, 2002)


class Datalake:
    def __init__(self):
        # self.datalake_root = Path(input("where?"))
        self.datalake_root = Path('../lake')

    def initialize(self):
        self._create_subdirectory('raw')
        self._create_subdirectory('raw/ghcnd')
        self._create_subdirectory('raw/ghcnd/daily')
        self._create_subdirectory('clean')
        self._create_subdirectory('clean/ghcnd')
        self._create_subdirectory('clean/ghcnd/daily')

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
        pass

    def _create_subdirectory(self, relative_path):
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

    def get_final_dataset_path(self):
        return self.datalake_root / paths["ghcnd_clean_stations"]

    def erase(self):
        pass

    def download_ghcnd(self):
        # download stations
        self._download_file(ghcnd_sources['stations'], self.datalake_root / paths["ghcnd_raw_stations"])
        # download daily
        for year in range(years[0], years[1] + 1):
            file_url = f'{ghcnd_sources["bucket"]}/csv.gz/by_year/{year}.csv.gz'
            dest_path = self.datalake_root / paths['ghcnd_raw_daily'] / f'{year}.csv.gz'
            self._download_file(file_url, dest_path)

    def clean_ghcnd_stations(self):
        clean_stations_file(self.datalake_root / paths["ghcnd_raw_stations"],
                            self.datalake_root / paths["ghcnd_clean_stations"])

    def clean_daily(self):
        for year in range(years[0], years[1] + 1):
            clean_daily_file(self.datalake_root / paths["ghcnd_raw_daily"] / f'{year}.csv.gz',
                             self.datalake_root / paths["ghcnd_clean_daily"] / f'{year}.parquet')

    def query(self):
        pass


def clean_stations_file(raw_path, clean_path):
    """
    Clean a single stations file
    :param raw_path:
    :param clean_path:
    """
    """
        Reads the ghcnd-stations fixed-width file, sets datatypes, and saves it as a parquet file.
        """
    stations = pd.read_fwf(raw_path, header=None,
                           colspecs=[(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71), (72, 75), (76, 79),
                                     (80, 85)])
    stations.columns = ['station_id', 'latitude', 'longitude', 'elevation', 'state', 'name', 'gsn_flag', 'hcn_crn_flag',
                        'wmo_id']
    stations['station_id'] = stations['station_id'].astype(str)
    stations['latitude'] = stations['latitude'].astype(float)
    stations['longitude'] = stations['longitude'].astype(float)
    stations['elevation'] = stations['elevation'].astype(float)
    stations['name'] = stations['name'].astype(str)
    stations.drop(columns=['state', 'gsn_flag', 'hcn_crn_flag', 'wmo_id'], inplace=True)

    stations.to_parquet(clean_path)


def drop_stations(df):
    # stations = pd.read_parquet(lake.)
    pass


def drop_daily_columns(df):
    pass


def process_dates(df):
    pass

def create_element_tables(df):
    pass

def join_element_tables(df):
    pass

def join_stations_elements(df):
    pass

def drop_station_columns(df):
    pass

def generate_geometries(df):
    pass

def clean_daily_file(raw_path, clean_path):
    """
    Clean a single daily file. each cleaning step should be a sub function
    :param raw_path:
    :param clean_path:
    """
    daily_dtypes = {'station_id': 'str', 'element': pd.CategoricalDtype(), 'm_flag': pd.CategoricalDtype(),
                    'q_flag': pd.CategoricalDtype(), 's_flag': pd.CategoricalDtype(), 'date': str, 'time': str,
                    'value': 'float'}
    df = pd.read_csv(raw_path, header=None,
                     names=['station_id', 'date', 'element', 'value', 'm_flag', 'q_flag', 's_flag', 'time'],
                     dtype=daily_dtypes, engine='pyarrow')
    # daily file cleaning steps:
    # 1. drop all non-North_American Stations
    df = drop_stations(df)
    # 2. drop unwanted columns
    df = drop_daily_columns(df)
    # 4. process dates
    df = process_dates(df)
    # 5. create element table
    df = create_element_tables(df)
    # 6. join elements into single table
    df = join_element_tables(df)
    # 7. join with stations
    df = join_stations_elements(df)
    # 8. drop unwanted columns
    df = drop_station_columns(df)
    # 9. generate geometries
    gdf = generate_geometries(df)
    gdf.to_parquet()

    # 10. write to disk
